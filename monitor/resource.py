import datetime

from errors import InvalidConfigError
from condition import ConditionFactory
from schedule import Schedule


class ResourceStatus(object):
    SUCCESS, FAIL = ('Success', 'Fail')


class MonitoredResource(object):

    def __init__(self, config):
        self.url = None
        self.schedule = None
        self.conditions = []

        self._load_config(config)

    def _load_config(self, config):
        if not config:
            raise InvalidConfigError(u'Invalid config file. The "site" section is missing.')
        url = config.get('url')
        if not url:
            raise InvalidConfigError(u'Invalid config file. The "url" section is missing.')
        self.url = url
        schedule = config.get('schedule')
        if not schedule:
            raise InvalidConfigError(u'Invalid config file. The "schedule" section is missing.')
        schedule = schedule.strip()
        if len(schedule.split()) != 5:
            raise InvalidConfigError(u'Invalid config file. {} is an invalid expression for '
                                     u'the "schedule" section'.format(schedule))
        self.schedule = Schedule(schedule)
        conditions = config.get('conditions')
        if not conditions:
            raise InvalidConfigError(u'Invalid config file. The "conditions" section is missing.')
        for con_type, con_value in conditions.items():
            if not con_type or not con_value:
                raise InvalidConfigError(u'Invalid config file. The "conditions" section is invalid.')
            self.conditions.append(ConditionFactory.factory(con_type, con_value))

    def is_ready(self):
        if self.schedule:
            return self.schedule.is_ready()
        return False


class ResourceResponse(object):

    def __init__(self, resource, status, response=None, duration=None, message=None):
        self.resource = resource
        self.status = status
        self.response = response
        self.duration = duration
        self.message = message
        self.last_check = datetime.datetime.now()

    @property
    def logger_info(self):
        return {
            'status': self.status,
            'response_time': self.duration if self.duration else None,
            'response_code': self.response.status_code if self.response else None,
            'url': self.resource.url,
        }

