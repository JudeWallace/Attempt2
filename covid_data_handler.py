# -*- coding: utf-8 -*-
"""All relevant covid statisitcal data is processed in this module.

This module deals with getting, via api call/accessing file, all the
statistical covid data and processing it so it can be displayed on the 
dashboard of the application
"""

import csv 
import json
import logging
from sched import Event
from uk_covid19 import Cov19API
from scheduler import s

# Logger for covid_data_handler modules
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)s: %(name)s: %(asctime)s - %(message)s"
)

file_handler = logging.FileHandler('backend_log.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def parse_csv_data(csv_filename: str) -> list or None:
    """
    Returns the data from inside the csv file

        Args:
            csv_filename (str): A string, which is the path of a file 

        Returns:
            data (list): list of each row of data in the csv file 
    """
    # Open csv file in read only mode
    try:
        logger.info("Reading csv file data")
        with open(csv_filename, mode='r') as f:
            reader = csv.reader(f)
            # Create a multidimenstional array of the files data
            data = list(reader)
        
        return data
    
    except:
        logger.exception("csv filepath not found")


def process_covid_csv_data(covid_csv_data: list) -> tuple or None:
    """
    Returns the required data from the static covid file and processes it 
    accordingly

        Args: 
            covid_csv_data (list): A list of strings containg all the data 
                                   grabbed by the API which is stored in the 
                                   covid_data_cache.csv file

        Returns:
            local7days_cases (int): Local 7 day infection rate, in the location 
                                    specified in the config file
            last7days_cases (int): National 7 day infection rate
            current_hospital_cases (int): Current hospital cases. Taken from 
                                          the national data
    """
    # Test data has been got from file correctly
    if covid_csv_data == []:
        logger.error("csv data not found")
        
    else:
        # Get cummulative 7days deaths
        last7days_cases = 0
        for i in range(len(covid_csv_data)):
            if covid_csv_data[i][-1] != '':
                # Skip the first line as is the headings of the columns
                if i == 0:
                    continue
                else:
                    for j in range(0, 7):
                        last7days_cases += int(covid_csv_data[j+i+1][-1])      
                    break

        # Get the hosptial cases from the previous day
        for i in range(len(covid_csv_data)):
            # Skip the first line as is the headings of the columns
            if i == 0:
                continue
            elif covid_csv_data[i][-2] != '':
                current_hospital_cases = int(covid_csv_data[i][-2])
                break

        # Get the cumulative num of death
        for j in range(len(covid_csv_data)):
            # Skip the first line as is the headings of the columns
            if j == 0:
                continue
            elif covid_csv_data[j][-3] != '':
                total_deaths = int(covid_csv_data[j][-3])
                break

        return last7days_cases, current_hospital_cases, total_deaths   


def process_API_data(covid_csv_data: list) -> tuple or int or None:
    """
    Checks which data is in the file, local or national. 
    Returns the required data from the API depended on if its local or national 
    data.

        Args: 
            covid_csv_data (list): A list of strings containg all the data 
                                   grabbed by the API which is stored in the 
                                   covid_data_cache.csv file
                                   
        Returns:
            local7days_cases (int): Local 7 day infection rate, in the location 
                                    specified in the config file
            last7days_cases (int): National 7 day infection rate
            current_hospital_cases (int): Current hospital cases. Taken from 
                                          the national data
            total_deaths (int): Current cumulative deaths. Also tajen from the 
                                national data
    """
    # Open config file to get local areaCode 
    with open('config.json', 'r') as json_file:
        data = json.load(json_file)
        json_data = data['covid_data']

    logger.info("Processing API data...")
    # Test data has been got from file correctly
    if covid_csv_data == []:
        logger.error("file is empty")
        return None
    
    # If local data is present continue to search for the required data
    elif covid_csv_data[1][0] == json_data["local_areaCode"]:
        local7days_cases = 0
        for i in range(len(covid_csv_data)):
            if covid_csv_data[i][-1] != '':
                if i == 0:
                    continue
                else:
                    for j in range(0, 7):
                        local7days_cases += int(covid_csv_data[j+i+1][-1])      
                    break
        
        return local7days_cases

    else:
        last7days_cases, current_hospital_cases, total_deaths = \
            process_covid_csv_data(covid_csv_data)

        return last7days_cases, current_hospital_cases, total_deaths
    
    
def covid_API_request(location='Exeter', location_type='ltla') -> dict:
    """
    Using the uk_covid19 module this function grabs the upto date data on 
    cornavirus. Once the api has grabbed the data the data is then saved to the 
    respective csv file, covid_data_cache.csv. To be accessed and minulapated 
    accordingly in the following functions
        
        Args:
            location (str): Is set as a default argumet
            location_type (str): Is also set as a default argument
        
        Returns:
            {"data": [api_data]} (dict): retuns the API data in a list which
                                         can be accessed by called data on the
                                         assigned variable
    """
    # Setting the filters for the api
    covid_API_filter = [
        'areaType=' + location_type,
        'areaName=' + location
    ]
    # Creating the structure of the api
    covid_API_structure = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCase": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate"
    }
    # Instantiation of the API
    api = Cov19API(filters=covid_API_filter, structure=covid_API_structure)
    # Extracting the data
    api_data = api.get_csv()
    
    logger.info("Getting covid API response")

    if api_data == ' ':
        logger.error("Covid API returned null")

    else:
        with open("covid_data_cache.csv", "w") as f:
            f.write(f"{api_data}")
        logger.info("Covid API data stored in cache file")
    
    return {"data": [api_data]}


def update_covid_data_json() -> True:
    """
    Returns all the relevant data the dasboard needs. Does this by calling the 
    covid_API_request function twice. Once to get the local data, then once 
    with specified paremeters for the national data required in the application

        Args:
            None 

        Returns:
            True
    """
    # Get local 7 day cases
    logger.info('covid_API_request local area call')
    covid_API_request()
    local7days_cases = process_API_data(parse_csv_data('covid_data_cache.csv'))  
    # Get the rest of the data needed from a national data
    logger.info('covid_API_request National area call')
    covid_API_request('England', 'nation')
    last7days_cases, current_hospital_cases, total_deaths = process_API_data(
        parse_csv_data('covid_data_cache.csv'))  

    logger.info("Returning covid data to dashboard")

    covid_data_dict = {
        "local7days_cases": local7days_cases, 
        "last7days_cases": last7days_cases, 
        "current_hospital_cases": current_hospital_cases,
        "total_deaths": total_deaths
    }
                        
    with open('dashboard_covid_data.json', 'w')as covid_json:
        json.dump(covid_data_dict, covid_json)

    return True


def dashboard_covid_data() -> tuple:
    """
    Reads the json file containg the covid statisical data and returns the 
    values

        Args:
            None 

        Returns:
            local7days_cases (int): Local 7 day infection rate, in the location 
                                    specified in the config file 
            last7days_cases (int): National 7 day infection rate
            current_hospital_cases (int): Current hospital cases. Taken from 
                                          the national data
            total_deaths (int): Current cumulative deaths. Also tajen from the 
                                national data
    """

    with open('dashboard_covid_data.json', 'r')as covid_json:
        data = json.load(covid_json)
        local7days_cases = data['local7days_cases']
        last7days_cases = data['last7days_cases']
        current_hospital_cases = data['current_hospital_cases']
        total_deaths = data['total_deaths']

    return local7days_cases, last7days_cases, current_hospital_cases, \
        total_deaths 


def schedule_covid_upadates(update_interval: int, update_name: str) -> Event:
    """
    Creates a scheduled update of the covid data, and adds it to the scheduler
    queue

        Args:
            update_interval (int): Delay of the interval in seconds
            update_name (str): Name of the update being created

        Returns:
            covid_update (Event): Returns the id of the event being scheduled
    """
    
    covid_update = s.enter(update_interval, 1, update_covid_data_json)
    return covid_update
    