# -*- coding: utf-8 -*-
"""This module is all the tests for the module covid_news_handling.py"""

from covid_news_handling import dashboard_news, news_API_request, update_news
from scheduler import s


def test_news_API_request() -> None:
    """Tests the news_API_requet function"""
    
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()


def test_update_news() -> None:
    """Tests the update_news function"""

    news_schedule = update_news('', 'Y', 10)
    assert news_schedule in s.queue
    s.cancel(news_schedule)


def test_dasboard_news() -> None:
    """Tests the dashboard_news function"""

    newsarticles = dashboard_news()
    assert len(newsarticles) <= 4
