import pytest
from freezegun import freeze_time

from errors import InvalidScheduleException
from schedule import MinuteMatcher, MonthMatcher, DayOfWeekMatcher, DayMatcher, HourMatcher, Matcher, Schedule


@pytest.mark.parametrize("expression,valid_range", [
        ('*', set(range(0, 60))),
        ('45', {45}),
        ('12-15', {12, 13, 14, 15}),
        ('*/15', {0, 15, 30, 45}),
        ('15,45,90', {15, 45})
    ])
def test_minute_matcher_valid_range(expression, valid_range):
    assert MinuteMatcher(expression).valid_range == valid_range


@pytest.mark.parametrize("expression,datetime,is_valid", [
    ('45', '2012-01-14 12:45', True),
    ('*/15', '2012-01-14 12:32', False)
])
def test_minute_matcher_is_valid(expression, datetime, is_valid):
    with freeze_time(datetime):
        assert MinuteMatcher(expression).is_valid() == is_valid


@pytest.mark.parametrize("expression,valid_range", [
        ('*', set(range(0, 24))),
        ('23', {23}),
        ('12-15', {12, 13, 14, 15}),
        ('*/8', {0, 8, 16}),
        ('23,24', {23})
    ])
def test_hour_matcher_valid_range(expression, valid_range):
    assert HourMatcher(expression).valid_range == valid_range


@pytest.mark.parametrize("expression,datetime,is_valid", [
    ('12', '2012-01-14 12:45', True),
    ('13-15', '2012-01-14 12:32', False)
])
def test_hour_matcher_is_valid(expression, datetime, is_valid):
    with freeze_time(datetime):
        assert HourMatcher(expression).is_valid() == is_valid


@pytest.mark.parametrize("expression,valid_range", [
        ('*', set(range(1, 32))),
        ('13', {13}),
        ('6-9', {6, 7, 8, 9}),
        ('*/10', {1, 11, 21, 31}),
        ('15,30,45', {15, 30})
    ])
def test_day_matcher_valid_range(expression, valid_range):
    assert DayMatcher(expression).valid_range == valid_range


@pytest.mark.parametrize("expression,datetime,is_valid", [
    ('11-15', '2012-01-14 12:45', True),
    ('*/2', '2012-01-14 12:32', False)
])
def test_day_matcher_is_valid(expression, datetime, is_valid):
    with freeze_time(datetime):
        assert DayMatcher(expression).is_valid() == is_valid


@pytest.mark.parametrize("expression,valid_range", [
        ('*', set(range(1, 8))),
        ('7', {7}),
        ('3-4', {3, 4}),
        ('*/3', {1, 4, 7}),
        ('6,7,8', {6, 7})
    ])
def test_day_of_week_matcher_valid_range(expression, valid_range):
    assert DayOfWeekMatcher(expression).valid_range == valid_range


@pytest.mark.parametrize("expression,datetime,is_valid", [
    ('6,7', '2012-01-14 12:45', True),
    ('1,2,3', '2012-01-14 12:32', False)
])
def test_day_of_week_matcher_is_valid(expression, datetime, is_valid):
    with freeze_time(datetime):
        assert DayOfWeekMatcher(expression).is_valid() == is_valid


@pytest.mark.parametrize("expression,valid_range", [
        ('*', set(range(1, 13))),
        ('6', {6}),
        ('6-9', {6, 7, 8, 9}),
        ('*/6', {1, 7}),
        ('6,12,18', {6, 12})
    ])
def test_month_matcher_valid_range(expression, valid_range):
    assert MonthMatcher(expression).valid_range == valid_range


@pytest.mark.parametrize("expression,datetime,is_valid", [
    ('*', '2012-01-14 12:45', True),
    ('4-11', '2012-01-14 12:32', False)
])
def test_day_of_week_matcher_is_valid(expression, datetime, is_valid):
    with freeze_time(datetime):
        assert MonthMatcher(expression).is_valid() == is_valid


@pytest.mark.parametrize("expression,", [
    '16/4',
    '*/*',
    '16/*',
    'a-11',
    '*-*',
    '*,*',
    'a'
])
def test_invalid_expressions(expression):
    with pytest.raises(InvalidScheduleException):
        Matcher.range = range(0)
        Matcher(expression)


@pytest.mark.parametrize("rules,is_ready", [
    ('* * * * *', True),
    ('32 13-17 * * *', False),
    ('30-40 12 14 1 6', True),
    ('* 12 13,14 1 1-5', False)
])
@freeze_time('2012-01-14 12:32')
def test_schedule_is_ready(rules, is_ready):
    assert Schedule(rules).is_ready() == is_ready
