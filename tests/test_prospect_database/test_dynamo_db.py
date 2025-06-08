from typing import Dict, Union

from unittest import mock

from asta_s_eu.scraping.core.prospect_database.dynamo_db import DynamoDB


class DynamoDBExtension(DynamoDB):
    """
    Add Clean-up method to DynamoDB class
    """

    def clean_test_data(self, prospect: Dict[str, str]) -> None:
        """Clean-up method to DynamoDB class"""
        self._db.delete_item(
            Key={
                'k': prospect['product_id'],
                's': 'x',
            }
        )


# pylint: disable=invalid-name,missing-function-docstring,too-few-public-methods
class MockedBoto3:
    """Mocking external AWS boto3 API"""

    # noinspection PyPep8Naming
    class Table:
        """Mocking external AWS boto3.table API"""

        def __init__(self, name: str) -> None:
            self._name = name
            self._data = {}

        def get_item(self, Key: Dict[str, str]) -> Dict[str, Union[str, Dict[str, str]]]:
            index = (
                ('k', Key['k']),
                ('s', Key['s']),
            )
            response = {
                'some-http-key': 'some-http-value'
            }
            value = self._data.get(index, None)

            if value:
                response['Item'] = value

            return response

        def delete_item(self, Key: Dict[str, str]):
            index = (
                ('k', Key['k']),
                ('s', Key['s']),
            )
            self._data.pop(index, None)

        def put_item(self, Item: Dict[str, str]) -> None:
            index = (
                ('k', Item['k']),
                ('s', Item['s']),
            )
            self._data[index] = Item
# pylint: enable=invalid-name,missing-function-docstring,too-few-public-methods

def test_crud_dynamodb():
    """
    Test Create, READ, UPDATE and DELETE use cases
    """
    banana_prospect = {
        'product_id': 'banana-id',
        'key': 'value'
    }

    db = DynamoDBExtension(MockedBoto3())
    db.clean_test_data(banana_prospect)

    # CREATE, READ, no UPDATE, no DELETE
    assert db.capture([banana_prospect]) == [banana_prospect]

    # no CREATE, READ, no UPDATE, no DELETE
    assert not db.capture([banana_prospect])

    # DELETE
    db.clean_test_data(banana_prospect)


def test_last_run_dynamodb():
    """
    Test less_than_24hour_ago feature
    """
    db = DynamoDBExtension(MockedBoto3())
    last_run_id = 'ebay-k'
    db.clean_test_data({
        'product_id': last_run_id
    })
    last_run = db.last_run(last_run_id)
    assert not last_run.successful_less_than_24hour_ago()
    assert not last_run.failed_less_than_24hour_ago_on_current_host()

    last_run.mark_successful_run()
    assert last_run.successful_less_than_24hour_ago()

    # first time failed on this host
    with mock.patch('socket.gethostname', return_value='not-this-one'):
        last_run.mark_failed_run_per_current_host()
    assert not last_run.failed_less_than_24hour_ago_on_current_host()

    # first time failed on this host
    last_run.mark_failed_run_per_current_host()
    assert last_run.failed_less_than_24hour_ago_on_current_host()

    # retry failed
    last_run.mark_failed_run_per_current_host()
    assert last_run.failed_less_than_24hour_ago_on_current_host()

    db.clean_test_data({
        'product_id': last_run_id
    })
