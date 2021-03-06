import re

from errors import ConditionError


class ConditionType(object):
    STATUS, CONTENT, REGEX = ('status', 'content', 'regex')


class ConditionFactory:

    @staticmethod
    def factory(con_type, con_value):
        if con_type == ConditionType.STATUS:
            return StatusCondition(con_value)
        elif con_type == ConditionType.CONTENT:
            return ContentCondition(con_value)
        elif con_type == ConditionType.REGEX:
            return RegexCondition(con_value)
        raise NotImplementedError('{} is not supported condition'.format(con_type))


class Condition:

    def validate(self, response):
        raise NotImplementedError


class StatusCondition(Condition):

    def __init__(self, status_code):
        self.status_code = int(status_code)

    def validate(self, response):
        if response.status_code != self.status_code:
            raise ConditionError("Invalid response code: {} "
                                 "(expected {})".format(response.status_code, self.status_code))


class ContentCondition(Condition):

    def __init__(self, content):
        self.content = content

    def validate(self, response):
        if self.content not in response.text:
            raise ConditionError("The string hasn't been found.".format(self.content))


class RegexCondition(Condition):

    def __init__(self, pattern):
        self.pattern = re.compile(pattern)

    def validate(self, response):
        match = self.pattern.search(response.text)
        if not match:
            raise ConditionError("The regex hasn't been matched.".format(self.pattern))
