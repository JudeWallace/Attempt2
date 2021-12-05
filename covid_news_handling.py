# -*- coding: utf-8 -*-
"""All covid news is found and processed in this module.

This module is responosble for using a news api to get the upto date
headlines off the news source specified in the config file. The words
the api looks for in the title of the news article is set to
'Covid COVID-19 coronavirus' as default, however when calling the function
other phrases can be parsed in. Once the news is wrote to the corresponding
json file, the rest of the module processes the articles grabbed and returns
them to the dashboard to be desplayed. In this module it also deals with 
scheduling the upating of the news and removing artcile which the user has 
specified to remove, which is then returned back to the dasboard so it can be 
updated accordindly
"""
from sched import Event
import flask
import requests
import json
from datetime import date
import logging
from scheduler import s

# Logger for covid_news_handling module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)s:%(name)s:%(asctime)s - %(message)s"
)

file_handler = logging.FileHandler('backend_log.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def news_API_request(covid_terms='Covid COVID-19 coronavirus') -> True:
    """
    Using news API settings specified in thec config file to search for news 
    articles with the key terms parsed to the functions. Which is then wrote to 
    the respective json file

        Args:
            covid_terms (str): The phrases in which it looks up in the news
        
        Returns:
            True
    """
    # Replace the spaces in the string with OR/+/-
    covid_terms = covid_terms.replace(" ", " OR ")
    
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
        news_config = data['news']

    # Define endpoint 
    url = 'https://newsapi.org/v2/everything'

    # Specify the parameters of the API
    parameters = {
        'qInTitle': covid_terms,
        'sources': news_config['news_source'],
        'from': date.today().strftime('%Y-%m-%d'), 
        'sortBy': 'relevacny',
        'language': news_config['language']
    }

    # Using KEY in header to hide it from url
    headers = {
        'X-API-KEY': news_config['API_KEY']
    }
    # Make the request
    response = requests.get(url, params=parameters, headers=headers)
    
    try:
        response.raise_for_status()
        logger.info("Testing news API didn't through any error...")

    except requests.exceptions.HTTPError as errh:
        logger.error("An Http Error occurred:" + repr(errh))

    except requests.exceptions.ConnectionError as errc:
        logger.error("An Error Connecting to the API occurred:" + repr(errc))

    except requests.exceptions.Timeout as errt:
        logger.error("A Timeout Error occurred:" + repr(errt))

    except requests.exceptions.RequestException as err:
        logger.error("An Unknown Error occurred" + repr(err))

    # Convert the response to JSON format 
    response_json = response.json()

    logger.info("Successful news API call")

    # Check the api request hasn't encountered an error
    if response_json['status'] != 'error':
        
        with open('covid_news_data.json', 'w')as f:
            json.dump(response_json, f)

        logger.info(
            str(response_json['status']) + ' -Sucessfully grabbed news'
        )
    else:
        logger.error(
            str(response_json['status']) + ' -Occured when grabbing news'
        )

    return True


def update_news(removed_article: str, schedule_update='N', update_interval=0) \
     -> list or Event:
    """
    Removes the article specified to be removed by the user and rewrites the 
    news json file without the removed article in. Then returns all the 
    remaining articles. 
    Any update of data requested is also created as an event in the scheduler.
    Then returns the event id 

        Args:
            removed_article (str): The title of the article wanting to be 
                                   removed off the application

        Returns:
            updated_news_list (list): List of dicionaires containg all the news 
                                      articles, not including the one parsed 
                                      into the function to be removed
            news_update_id (Event): The event id of the newly created event
    """
    # Check if an Event needs to be scheduled
    if schedule_update == 'Y':
        logger.info("Creating news update event...")
        news_update_id = s.enter(update_interval, 1, news_API_request)
        return news_update_id

    logger.info("Getting current news from dashboard...")

    with open('covid_news_data.json', "r") as file:
        news = json.load(file)

    news_list = news.pop('articles')

    # Remove article from file and decrease article counter
    for i in range(len(news_list)):
        if news_list[i]['title'] == removed_article:
            del news_list[i]
            news['articles'] = news_list
            news['totalResults'] -= 1
            with open('covid_news_data.json', 'w') as update_json:
                json.dump(news, update_json)
            break

    # Removed news shouldnt appear when the data strucutre is updated
    logger.info('Sending updated news titles to the dasboard')
    updated_news_list = dashboard_news()

    return updated_news_list


def dashboard_news() -> list:
    """
    Returns a list of dicionaries comtaing the news title and description.
    Limit set on how many news articles are appended to the list is 5

        Args:
            None
        
        Returns:
            articles (list): Contains dictionries of news titles and desciption
                             with the link to the page added to the contents
                             using flask markup
                            
    """

    with open('covid_news_data.json', 'r') as f:
        news_dict = json.load(f)
        articles = news_dict["articles"]
        for article in articles:
                article['content'] = flask.Markup(article['description'] + 
                ' ' + '<a href=' + article['url'] + '>Read more</a>')
                
    # Add a limit to the maximum number of artciles shown at once
    if len(articles) > 4:
        articles = articles[:4]
    
    return articles
