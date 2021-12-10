# -*- coding: utf-8 -*-
"""This module is all the tests for the module covid_data_handler.py"""

import pytest
from covid_data_handler import *
from scheduler import s


def test_parse_csv_data() -> None:
    """Tests the parse_csv_data function"""
    # Matts test
    data = parse_csv_data('nation_2021-10-28.csv') 
    assert len(data) == 639


def test_process_covid_csv_data() -> None:
    """Tests the parse_csv_data function"""
    # Matts test
    last7days_cases, current_hospital_cases, total_deaths = \
        process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))  
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019 
    assert total_deaths == 141_544


def test_process_API_data() -> None:
    """Tests the process_API_data function"""

    covid_API_request()
    local7days_cases = process_API_data(parse_csv_data('covid_data_cache.csv'))
    assert isinstance(local7days_cases, int)

    covid_API_request('England', 'nation')
    last7days_cases, current_hospital_cases, total_deaths = \
        process_API_data(parse_csv_data('covid_data_cache.csv'))  
    assert isinstance(local7days_cases, int)
    assert isinstance(last7days_cases, int)
    assert isinstance(current_hospital_cases, int)
    assert isinstance(total_deaths, int)


def test_covid_API_request() -> None:
    """Tests the covid_API_request function"""

    assert covid_API_request()
    assert covid_API_request('Exeter', 'ltla') == covid_API_request()

    # Matts test
    data = covid_API_request()
    assert isinstance(data, dict)


def test_dashboard_covid_data() -> None:
    """Tests the dashboard_covid_data function"""

    assert dashboard_covid_data()
    assert isinstance(dashboard_covid_data(), tuple)
    local7days_cases, last7days_cases, current_hospital_cases, total_deaths = \
        dashboard_covid_data()
    assert isinstance(local7days_cases, int)
    assert isinstance(last7days_cases, int)
    assert isinstance(current_hospital_cases, int)
    assert isinstance(total_deaths, int)


def test_schedule_covid_upadates() -> None:

    """Tests the schedule_covid_upadates function"""
    # Matts test
    schedule_covid_upadates(update_interval=10, update_name='update test')

    covid_schedule = schedule_covid_upadates(1, "testing function")
    assert covid_schedule in s.queue
    s.cancel(covid_schedule)
    