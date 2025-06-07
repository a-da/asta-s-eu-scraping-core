from unittest import mock

import pytest

from asta_s_eu.scraping.core import helper


def test_activate_coupons_just_once_per_day_by_dynamodb():
    """
    4 test suits cases for testing 'less_than_24hour_ago' feature
    """
    activate_coupons_callback = mock.Mock()
    with mock.patch.object(helper, 'ProspectDatabase') as prospect_database:
        last_run = mock.Mock(xxx='last_run')
        prospect_database.return_value.last_run = last_run

        # ++ case 1
        # + GIVEN
        last_run.reset_mock()
        activate_coupons_callback.reset_mock()
        last_run.return_value.successful_less_than_24hour_ago.return_value = True
        # WHEN
        helper.activate_coupons_just_once_per_day_by_dynamodb('key', activate_coupons_callback)
        # THEN
        assert len(last_run.mock_calls) == 2

        # ++ case 2
        # + GIVEN
        last_run.reset_mock()
        activate_coupons_callback.reset_mock()
        last_run.return_value.successful_less_than_24hour_ago.return_value = False
        last_run.return_value.failed_less_than_24hour_ago_on_current_host.return_value = True
        # WHEN
        helper.activate_coupons_just_once_per_day_by_dynamodb('key', activate_coupons_callback)
        # THEN
        assert len(last_run.mock_calls) == 3
        activate_coupons_callback.assert_not_called()

        # ++ case 3
        # + GIVEN
        last_run.reset_mock()
        activate_coupons_callback.reset_mock()
        last_run.return_value.successful_less_than_24hour_ago.return_value = False
        last_run.return_value.failed_less_than_24hour_ago_on_current_host.return_value = False
        # WHEN
        helper.activate_coupons_just_once_per_day_by_dynamodb('key', activate_coupons_callback)
        # THEN
        assert len(last_run.mock_calls) == 4
        activate_coupons_callback.assert_called_once()
        last_run.return_value.mark_successful_run.assert_called_once()

        # ++ case 4
        # + GIVEN
        last_run.reset_mock()
        activate_coupons_callback.reset_mock()
        activate_coupons_callback.side_effect = Exception('some exceptions')
        last_run.return_value.successful_less_than_24hour_ago.return_value = False
        last_run.return_value.failed_less_than_24hour_ago_on_current_host.return_value = False
        # WHEN
        with pytest.raises(Exception):
            helper.activate_coupons_just_once_per_day_by_dynamodb('key', activate_coupons_callback)
        # THEN
        assert len(last_run.mock_calls) == 4
        activate_coupons_callback.assert_called_once()
        last_run.return_value.mark_successful_run.assert_not_called()
        last_run.return_value.mark_failed_run_per_current_host.assert_called_once()
