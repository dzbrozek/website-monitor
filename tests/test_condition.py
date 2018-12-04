import pytest

from condition import StatusCondition, ContentCondition, RegexCondition
from errors import ConditionError


class MockResponse:

    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


def test_status_condition():
    condition = StatusCondition(200)
    response = MockResponse(status_code=200, text='')

    condition.validate(response)

    response = MockResponse(status_code=404, text='')

    with pytest.raises(ConditionError) as cm:
        condition.validate(response)

    assert cm.value.message == 'Invalid response code: 404 (expected 200)'


def test_content_condition():
    condition = ContentCondition('can be only one')
    response = MockResponse(status_code=200, text='In the end, there can be only one')

    condition.validate(response)

    response = MockResponse(status_code=200, text='What about two?')

    with pytest.raises(ConditionError) as cm:
        condition.validate(response)

    assert cm.value.message == 'The string hasn\'t been found.'


def test_regex_condition():
    pattern = r"I'm \d+ years old"
    condition = RegexCondition(pattern)
    response = MockResponse(status_code=200, text='My name is John and I\'m 16 years old.')

    condition.validate(response)

    response = MockResponse(status_code=200, text='My name is John and I\'m too old.')

    with pytest.raises(ConditionError) as cm:
        condition.validate(response)

    assert cm.value.message == 'The regex hasn\'t been matched.'.format(pattern)
