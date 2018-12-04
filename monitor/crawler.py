import requests
import time

from errors import ConditionError
from resource import ResourceResponse, ResourceStatus


class Crawler:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'
    }

    def __init__(self, resource):
        self.resource = resource

    def check(self):
        try:
            start = time.time()
            response = requests.get(self.resource.url, headers=self.headers, timeout=10)
            elapsed = time.time() - start
            try:
                self._check_conditions(response)
            except ConditionError as e:
                return ResourceResponse(resource=self.resource, status=ResourceStatus.FAIL,
                                        response=response, duration=elapsed, message=e.message)
            else:
                return ResourceResponse(resource=self.resource, status=ResourceStatus.SUCCESS,
                                        response=response, duration=elapsed)
        except requests.exceptions.RequestException:
            return ResourceResponse(resource=self.resource, status=ResourceStatus.FAIL,
                                    message='Connection error. Unable to check the website.')

    def _check_conditions(self, response):
        for condition in self.resource.conditions:
            condition.validate(response)
