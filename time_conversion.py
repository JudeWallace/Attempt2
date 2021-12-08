# -*- coding: utf-8 -*-
"""All conversions of time happens in this module.

This module is responsible for converting time formatted in the form 
"hours:minutes: and returning a positive integer value in seconds of how long 
it is away from the current time

Main implentation of this module is when setting the time delay for the 
scheduled updates
"""

import logging
import time

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


def interval_in_seconds(hhmm: str) -> int:
    """
    Returns the interval, in seconds, of which the scheduled event will be 
    delayed by

        Args:
            hhmm (str): The time selected by the user on the dashboard

        Returns:
            interval (int): The time delay for the scheduled event in seconds
    """

    logger.info('Working out period of interval...')
    current_time = hhmm_to_seconds(current_time_hhmm())
    time_of_update = hhmm_to_seconds(hhmm)
    
    if time_of_update < current_time:
        interval = (86400 - current_time) + time_of_update
    else:
        interval = time_of_update - current_time

    logger.info("Returning update period in seconds")
    return interval


def current_time_hhmm() -> str:
    """
    Uses the time library to get the current time in hours and minutes

        Args:
            None
        
        Returns:
            str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min) (str): 
            Current time formatted as hour:minutes
    """

    logger.info('Getting current time')
    return str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)


def minutes_to_seconds(minutes: str) -> int:
    """
    Converts minutes to seconds

        Args:
            minutes (str): minutes of the time string 
        
        Returns:
            int(minutes)*60 (int): minutes converted to seconds
    """

    logger.info('Returning minutes to seconds')
    return int(minutes)*60


def hours_to_minutes(hours: str) -> int:
    """
    Converts hours to minutes

        Args:
            hours (str): hours of the time string 
            
        Returns:
            int(hours)*60 (int): hours converted to minutes
    """
    
    logger.info('Returning hours to minutes')
    return int(hours)*60


def hhmm_to_seconds(hhmm: str) -> int:
    """
    Splits time which is formatted in a string to 2 seperate values hours and 
    minutes. Then performs the neccessary conversions to get them into seconds, 
    then they are added together 

        Args:
            hhmm (str): time formatted as "hours:minutes"

        Returns: minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) 
                 + \ minutes_to_seconds(hhmm.split(':')[1]) (int) : time in 
                 seconds
    """
    
    if len(hhmm.split(':')) != 2:
        logger.error('Incorrect format. Argument must be formatted as HH:MM')
        return None
    logger.info('Returing time from string to integer value in seconds')
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])
