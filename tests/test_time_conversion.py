# -*- coding: utf-8 -*-
"""This module is all the tests for the module time_conversion.py"""

import pytest
from time_conversion import*


def test_interval_in_seconds() -> None:
    """Tests the interval_in_seconds function"""
    
    interval = interval_in_seconds("13:00")
    assert type(interval) == int


def test_current_time_hhmm() -> None:
    """Tests the current_time_hhmm function"""

    assert current_time_hhmm()


def test_minutes_to_seconds() -> None:
    """Tests the minutes_to_seconds function"""

    assert minutes_to_seconds(1) == 60
    assert minutes_to_seconds(12) == 720


def test_hours_to_minutes() -> None:
    """Tests the hours_to_minutes function"""

    assert hours_to_minutes("24") == 1440


def test_hhmm_to_seconds() -> None:
    """Tests the hhmm_to_seconds function"""

    assert hhmm_to_seconds("12:04:0") is None
    assert hhmm_to_seconds("24:00") == 86400
