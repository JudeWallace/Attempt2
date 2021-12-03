# -*- coding: utf-8 -*-
"""Links the HTML template and backened to create the application

Within this module the event driven architecture is created. The module deals 
with all user inputs, processes them and does then complete corresponding task. 
It takes use of the python module flask to render the HTML bootstrap template.
"""
# Imports required
import json
from flask import Flask, render_template, request
import logging

from covid_data_handler import covid_API_request, dashboard_covid_data
from covid_data_handler import schedule_covid_upadates
from covid_news_handling import dashboard_news, news_API_request, update_news
from routine_tests import run_tests
from time_conversion import interval_in_seconds
from scheduler import s

# Create app flask object
app = Flask(__name__)

# Update all the news articles and cases data when application is first loaded
covid_API_request()
news_API_request()

# Global variables
TESTING = run_tests()
SCHEDULEDUPDATES = []
NEWS = None
LOCAL7DAY_CASES = None
LAST7DAYS_CASES = None
CURRENT_HOSPTIAL_CASES = None
TOTAL_DEATHS = None

# Get the data from config file
with open('config.json', 'r') as json_file:
    data = json.load(json_file)
    dasboard_config = data['dashboard']

# Run the logger if app not in debug mode
if not app.debug:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(levelname)s: %(name)s: %(asctime)s - %(message)s"
    )

    file_handler = logging.FileHandler('frontend_log.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


@app.route("/")
@app.route("/index", methods=['GET', 'POST'])
def submitted_form() -> str:
    """
    This module is the event driven architecture of the application. It takes
    in inputs from the user and does the corresponding task dependent on what
    event has been triggered/scheduled

        Args:
            None
        
        Returns:
            (function) render_template() -> str: Renders the html template in
                                                 the templated folder with the
                                                 given content
        
    """

    global TESTING

    logger.info("Page refreshed")
    s.run(blocking=False)

    NEWS = dashboard_news()
    LOCAL7DAY_CASES, LAST7DAYS_CASES, CURRENT_HOSPTIAL_CASES, TOTAL_DEATHS = (
        dashboard_covid_data()
    )
    logger.info("Current data retrieved from news and data modules")
    # Get data out of the url
    update_label = request.args.get('two')
    remove_article = request.args.get('notif')
    remove_schedule = request.args.get('update_item')
    
    if remove_article:
        logger.info(f'Article requeted to be removed: {remove_article}')
        NEWS = update_news(remove_article)
        logger.info("Article removed")
    
    elif remove_schedule:
        logger.info('Shecudle requested to be removed')
        for i in range(len(SCHEDULEDUPDATES)):
            if SCHEDULEDUPDATES[i]['title'] == remove_schedule:
                news_event_id = SCHEDULEDUPDATES[i]['newsID']
                data_event_id = SCHEDULEDUPDATES[i]['dataID']
                # Checks which events and event id are in the schedueled 
                # update and cancel them in the scheduler
                if news_event_id is not None and data_event_id is not None:
                    logger.info(
                        f"Removing specified event {SCHEDULEDUPDATES[i]}"
                    )
                    try:
                        s.cancel(news_event_id)
                        s.cancel(data_event_id)
                    except ValueError:
                        logger.warning("Event Not in queue")

                elif news_event_id is not None and data_event_id is not None:
                    logger.info(
                        f"Removing specified event {SCHEDULEDUPDATES[i]}"
                    )
                    try:
                        s.cancel(news_event_id)
                    except ValueError:
                        logger.warning("Event Not in queue")

                elif data_event_id is not None and news_event_id is None:
                    logger.info(
                        f"Removing specified event {SCHEDULEDUPDATES[i]}"
                    )
                    try:
                        s.cancel(data_event_id)
                    except ValueError:
                        logger.warning("Event Not in queue")

                # Delete the schedule from the dictionary
                del SCHEDULEDUPDATES[i]
                break

    elif update_label:

        time_update = request.args.get('update')
        repeat_update = request.args.get('repeat')
        update_data = request.args.get('covid-data')
        update_news_headlines = request.args.get('news')

        logger.info('Update form submitted')
        logger.info('Processing form submitted')

        # Check there is at least one of the update boxes selected
        if update_data is None and update_news_headlines is None and (
            repeat_update is None
        ):
            logger.warning(
                "Schedule tried to be created with no events selected"
            )

        elif update_news_headlines is not None or update_data is not None:
            if time_update:
                # Check no update has the same name
                update_already_set = False
                for i in range(len(SCHEDULEDUPDATES)):
                    if SCHEDULEDUPDATES[i]['title'] == update_label:
                        logger.warning(
                            "Schedule tried to be created with the same label"
                        )
                        update_already_set = True
                        break
                # If no update has the same name, create the scheduled update
                if not update_already_set:
                    schedule_content = (
                        f'At {time_update} the following updates will run: '
                    )
                    if update_data and update_news_headlines:
                        schedule_content += 'Covid data, News articles '
                    elif update_news_headlines:
                        schedule_content += 'News articles '  
                    elif update_data:
                        schedule_content += 'Covid data '
                    if repeat_update:
                        schedule_content += 'and repeated until cancelled'
                        
                    # Get time of the interval in seconds from current time
                    interval = interval_in_seconds(time_update)

                    news_id = None
                    data_id = None

                    # If news box checked, create a news schedule
                    if update_news_headlines:
                        news_id = update_news(
                            None, schedule_update='Y', update_interval=interval
                        )
                        logger.info(f"News update scheduled for {time_update}")

                    # If covid data update checked, create a covid data 
                    # schedule
                    if update_data:
                        data_id = schedule_covid_upadates(
                            update_interval=interval,
                            update_name=update_label
                            )
                        logger.info(
                            f"Covid data update scheduled for {time_update}"
                        )
                
                    # Add schedule to dicionary
                    SCHEDULEDUPDATES.append({
                        "title": update_label, 
                        "content": schedule_content, 
                        "newsID": news_id, 
                        "dataID": data_id,
                        "repeat": repeat_update,
                        "timeofupdate": time_update
                        })
            else:
                logger.warning("Form submitted with no time attribute")

    # Check schedulded event is still in the queue
    events = s.queue
    delete = False
    for i in range(len(SCHEDULEDUPDATES)):
        # Check if news event has not been run, by looking for the id in the 
        # scheduler queue
        if SCHEDULEDUPDATES[i]['newsID'] is not None:
            if SCHEDULEDUPDATES[i]['newsID'] in events:
                logger.info(f"Event {SCHEDULEDUPDATES[i]} still in queue")
            else:
                # If repeat is True create a new covid data schedule 
                if SCHEDULEDUPDATES[i]['repeat'] == 'repeat':
                    interval_repeat = interval_in_seconds(
                        SCHEDULEDUPDATES[i]['timeofupdate']
                    )
                    if SCHEDULEDUPDATES[i]['newsID'] is not None:
                        repeated_news_id = update_news(
                            None, schedule_update='Y',
                            update_interval=interval_repeat
                        )
                        # Update dicionary with new event id
                        SCHEDULEDUPDATES[i]['newsID'] = repeated_news_id
                        logger.info(
                            f"Event {SCHEDULEDUPDATES[i]} event retriggred"
                        )
                else:
                    logger.info(f"Removing run event {SCHEDULEDUPDATES[i]}")
                    delete = True

        # Check if covid data event has not been run, by looking for the id in 
        # the scheduler queue
        if SCHEDULEDUPDATES[i]['dataID'] is not None:
            if SCHEDULEDUPDATES[i]['dataID'] in events:
                logger.info(f"Event {SCHEDULEDUPDATES[i]} still in queue")
            else:
                # If repeat is True create a new covid data schedule
                if SCHEDULEDUPDATES[i]['repeat'] == 'repeat':
                    interval_repeat = interval_in_seconds(
                        SCHEDULEDUPDATES[i]['timeofupdate']
                    )
                    if SCHEDULEDUPDATES[i]['dataID'] is not None:
                        repeated_news_id = update_news(
                            None, 
                            schedule_update='Y', 
                            update_interval=interval_repeat
                        )
                        # Update dicionary with new event id
                        SCHEDULEDUPDATES[i]['newsID'] = repeated_news_id
                        logger.info(
                            f"Event {SCHEDULEDUPDATES[i]} event retriggred"
                        )
                else:
                    logger.info(f"Removing run event {SCHEDULEDUPDATES[i]}")
                    delete = True

        # If schedule has been run and is not required to repeat, delete it 
        # from the schedule  
        if delete:
            del SCHEDULEDUPDATES[i]
        
    # Check if routine test have beens scheduled, if not schedule it
    if TESTING not in s.queue:
            TESTING = run_tests()

    return render_template(
        "index.html", 
        title='Covid-19 Statistics', 
        location=dasboard_config['local_location'],
        local_7day_infections=LOCAL7DAY_CASES,
        nation_location=dasboard_config['national_location'],
        national_7day_infections=LAST7DAYS_CASES,
        hospital_cases='Hospital cases: ' + str(CURRENT_HOSPTIAL_CASES), 
        deaths_total='Total deaths: ' + str(TOTAL_DEATHS),
        news_articles=NEWS, updates=SCHEDULEDUPDATES, 
        favicon='./static/images/covid_icon.png'
    )
    
    
if __name__ == '__main__':
    app.run(debug=False)
