import pytest
import requests
import responses

from crawler import Crawler
from errors import ConditionError
from resource import ResourceStatus


class MockResource:

    def __init__(self, url, conditions):
        self.url = url
        self.conditions = conditions


@pytest.fixture()
def my_resource():
    return MockResource('https://twitter.com/', [])


class MockConditionError:
    def __init__(self, *args, **kwargs):
        raise ConditionError('Invalid condition')


@responses.activate
def test_condition_error(my_resource, monkeypatch):
    responses.add(responses.GET, 'https://twitter.com/', status=200)

    monkeypatch.setattr("crawler.Crawler._check_conditions", MockConditionError)

    response = Crawler(my_resource).check()

    assert response.status == ResourceStatus.FAIL
    assert response.message == 'Invalid condition'
    assert response.response


@responses.activate
def test_request_error(my_resource):
    responses.add(responses.GET, 'https://twitter.com/', body=requests.exceptions.RequestException())

    response = Crawler(my_resource).check()

    assert response.status == ResourceStatus.FAIL
    assert response.message == 'Connection error. Unable to check the website.'
    assert response.response is None


@responses.activate
def test_valid_condition(my_resource):
    responses.add(responses.GET, 'https://twitter.com/', status=200)

    response = Crawler(my_resource).check()

    assert response.status == ResourceStatus.SUCCESS
    assert response.message is None
    assert response.response
