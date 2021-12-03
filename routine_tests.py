# -*- coding: utf-8 -*-
"""Runs tests to check the funcionalltiy of the code.

This module runs a select amount of tests on the backend code periodically to
check all the responses from the functions/modules are correct, and will flag 
errors if the code has been changed in a function/module that isn't working as 
intially indeed
"""

from sched import Event
from tests.test_time_conversion import *
from tests.test_covid_news_handling import *
from tests.test_covid_data_handler import *
from scheduler import s

# Logger for covid_news_handling module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)s:%(name)s:%(asctime)s - %(message)s"
)

file_handler = logging.FileHandler('routine_tests.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def tests_scheduled_backend() -> None:
    """
    Tests to be run on the code when called by the schedules

        Args:
            None
        
        Returns:
            None
    """

    try:
        logger.info("Running routine tests...")
        # Test data module key functions
        logger.info("Testing covid_data_handler")
        test_process_covid_csv_data()
        test_covid_API_request()
        test_schedule_covid_upadates()

        logger.info("covid_data_handler Passed")

        # Test news module key functions
        logger.info("Testing covid_data_handler")
        test_news_API_request()
        test_update_news()

        logger.info("covid_news_handling Passed")
        
        # Test time conversion module key functions
        logger.info("Testing covid_data_handler")
        test_hhmm_to_seconds()
        test_interval_in_seconds()
        logger.info("time_conversion Passed")

    except AssertionError as er:
        logger.error(f'Assertion error when testing: {er}')
    

def run_tests() -> Event:
    """
    Creates the event for the testing cycle. Event cycle will occure at 6am
    everyday

        Args:
            None
        
        Returns:
            test_schedule (Event): The event id of the testing schedule
    """

    logger.info("Creating routine testing event")

    interval = interval_in_seconds("6:00")
    test_schedule = s.enter(interval, 2, tests_scheduled_backend)
    logger.info(f"Event created {test_schedule}")

    return test_schedule
