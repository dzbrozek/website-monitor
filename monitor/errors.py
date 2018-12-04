
class InvalidConfigError(Exception):
    pass


class ConditionError(Exception):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidScheduleException(Exception):
    pass
