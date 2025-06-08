# pylint: disable=missing-class-docstring,protected-access
from typing import Iterable

from contextlib import nullcontext as does_not_raise
from unittest import mock

import pytest

from asta_s_eu.scraping.core.selenium import base_classes


class DummyImplementationOfSeleniumBot(base_classes.SeleniumBot):

    def open_home_page(self) -> None:
        pass

    def accept_cookie_if_needed(self) -> None:
        pass

    def login_if_needed(self, user: str, password: str) -> None:
        pass


class DummyImplementationOfCouponsSeleniumBot(DummyImplementationOfSeleniumBot):
    # pylint: disable=missing-function-docstring
    def open_e_coupons(self) -> None:
        pass

    def activate_e_coupons(self, *partners: str) -> Iterable[str]:
        pass


# commented api
# @pytest.mark.parametrize('browser_version, raise_exc', (
#     pytest.param('114.0.5735.198', does_not_raise(), id='exact_match'),
#     pytest.param(
#         '200.0.5735.198',
#         pytest.raises(
#             AssertionError,
#             match='google chrome version 200.0 is different than 114.0, '
#         ),
#         id="not_match"
#     ),
# ))
# def test_check_chrome_compatibility(browser_version: str, raise_exc):
#     """
#     GIVEN exact_match and not_match inputs
#     WHEN open the api implementation of Selenium Bot
#     THEN ensure the expected input match expected match
#     """
#     driver = mock.Mock()
#     driver.caps = {
#         'browserVersion': browser_version,
#         'chrome': {
#             'chromedriverVersion': '114.0.5735.90 (38...9-refs/branch-heads/5735@{#1052})'
#         }
#     }
#
#     with raise_exc:
#         with DummyImplementationOfSeleniumBot(driver=driver) as bot:
#             bot.open_home_page()


def test_without_driver_argument():
    """
    GIVEN the Implementation of Selenium Bot
    WHEN not provide webdriver instance
    THEN ensure that Implementation of Selenium Bot self create webdriver
    """
    with mock.patch.object(base_classes.webdriver, "Chrome") as chrome:
        bot = DummyImplementationOfSeleniumBot(headless=False)
        assert bot._driver == chrome.return_value


def test_random_human_sleep():
    """
    GIVEN the Implementation of Selenium Bot
    WHEN random_human_sleep
    THEN ensure that Implementation of Selenium Bot self create webdriver
    """
    with mock.patch.object(base_classes.time, "sleep") as sleep:
        bot = DummyImplementationOfCouponsSeleniumBot(driver=mock.Mock())
        bot.random_human_sleep(0)
        sleep.assert_called_once() # 1, 2, or 3

def test_mark_element():
    """
    GIVEN the Implementation of Selenium Bot
    WHEN mark an element
    THEN element is colored
    """
    driver = mock.Mock()
    bot = DummyImplementationOfCouponsSeleniumBot(driver=driver)
    element = mock.Mock()
    bot._mark_element(element)

    assert driver.execute_script.call_count == 3


@pytest.mark.parametrize('find', ([], ['One'], ['One', 'Two']))
def test_find_optional_element(find):
    """
    GIVEN the Implementation of Selenium Bot

    WHEN find an element
    THEN element is returned

    WHEN element is not find
    THEN null returned
    """
    driver = mock.Mock()
    driver.find_elements.return_value = find

    bot = DummyImplementationOfCouponsSeleniumBot(driver=driver)

    if len(find) > 1:
        raise_exc = pytest.raises(AssertionError)
    else:
        raise_exc = does_not_raise()

    with raise_exc:
        element = bot._find_optional_element('some-value')

        if find:
            assert element == find[0]
        else:
            assert not element
