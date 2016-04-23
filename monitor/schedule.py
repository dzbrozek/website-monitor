import datetime
import re

from errors import InvalidScheduleException


class Stack(object):

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop(0)

    def insert(self, index, item):
        self.items.insert(index, item)

    def size(self):
        return len(self.items)

    def first(self):
        return self.items[0]

    def empty(self):
        return not self.size()


class Matcher(object):

    def __init__(self, expression):
        self.operators = [',', '-', '/']
        self.operator_stack = Stack()
        self.operand_stack = Stack()
        self.valid_range = []
        self.expression = expression
        self.parse_expression()

    def is_valid(self):
        raise NotImplementedError()

    def parse_expression(self):
        for char in re.split(r'([{}])'.format(''.join(self.operators)), self.expression):
            if char in self.operators:
                self.operator_stack.push(char)
            else:
                try:
                    if char == "*":
                        self.operand_stack.push(char)
                        continue
                    self.operand_stack.push(int(char))
                except (ValueError, TypeError):
                    raise InvalidScheduleException(u'{} is not a number'.format(char))
        # special cases
        if self.operator_stack.size() == 0 and self.operand_stack.size() == 1:
            if isinstance(self.operand_stack.first(), int):
                self.valid_range = {self.operand_stack.pop()}  # 13
            elif self.operand_stack.first() == "*":
                self.valid_range = set(self.range)
            return

        while not self.operator_stack.empty():
            operator = self.operator_stack.pop()
            first_operand, second_operand = self.operand_stack.pop(), self.operand_stack.pop()
            if operator == ",":
                self.comma_operator(first_operand, second_operand)
            elif operator == "/":
                self.slash_operator(first_operand, second_operand)
            elif operator == "-":
                self.range_operator(first_operand, second_operand)

        if self.operand_stack.size() != 1:
            raise InvalidScheduleException(u'{} is invalid expression'.format(self.expression))

        self.valid_range = set(self.range) & set(self.operand_stack.pop())

    def comma_operator(self, first_operand, second_operand):
        if first_operand == "*":
            first_operand = list(self.range)
        elif isinstance(first_operand, int):
            first_operand = [first_operand]
        if second_operand == "*":
            second_operand = list(self.range)
        elif isinstance(second_operand, int):
            second_operand = [second_operand]

        result = first_operand + second_operand
        self.operand_stack.insert(0, sorted(set(result)))

    def range_operator(self, first_operand, second_operand):
        if first_operand == "*":
            first_operand = list(self.range)
        elif isinstance(first_operand, int):
            first_operand = [first_operand]
        if not isinstance(second_operand, int):
            raise InvalidScheduleException(u'{} is invalid expression'.format(self.expression))

        result = first_operand + range(first_operand[-1], second_operand + 1)
        self.operand_stack.insert(0, sorted(set(result)))

    def slash_operator(self, first_operand, second_operand):
        if first_operand == "*":
            first_operand = list(self.range)
        elif isinstance(first_operand, int):
            first_operand = [first_operand]
        if not isinstance(second_operand, int):
            raise InvalidScheduleException(u'{} is invalid expression'.format(self.expression))
        result = first_operand[::second_operand]
        self.operand_stack.insert(0, sorted(set(result)))


class MinuteMatcher(Matcher):
    range = range(0, 60)

    def is_valid(self):
        return datetime.datetime.now().minute in self.valid_range


class HourMatcher(Matcher):
    range = range(0, 24)

    def is_valid(self):
        return datetime.datetime.now().hour in self.valid_range


class DayMatcher(Matcher):
    range = range(0, 32)

    def is_valid(self):
        return datetime.datetime.now().day in self.valid_range


class DayOfWeekMatcher(Matcher):
    range = range(1, 8)

    def is_valid(self):
        return datetime.datetime.now().isoweekday() in self.valid_range


class MonthMatcher(Matcher):
    range = range(1, 13)

    def is_valid(self):
        return datetime.datetime.now().month in self.valid_range


class Schedule(object):

    def __init__(self, rules):
        self.rules = rules.strip().split()
        minute, hour, day, month, day_of_week = self.rules
        self.matchers = [
            MinuteMatcher(minute),
            HourMatcher(hour),
            DayMatcher(day),
            DayOfWeekMatcher(day_of_week),
            MonthMatcher(month)
        ]

    def is_ready(self):
        for matcher in self.matchers:
            if not matcher.is_valid():
                return False
        return True

