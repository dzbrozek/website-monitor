import argparse
import logging
from collections import OrderedDict

import gevent
import yaml
from gevent import queue, pool, event
from gevent.wsgi import WSGIServer
from jinja2 import Environment, PackageLoader

from crawler import Crawler
from errors import InvalidConfigError
from resource import MonitoredResource

logger = logging.getLogger('monitor')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(url)s %(status)s %(response_code)s %(response_time).2fs %(message)s')


class Monitor(object):

    def __init__(self):
        # tasks
        self.workq = queue.Queue()
        self.pool = pool.Pool(10)
        self.scheduler = None
        self.supervisor = None
        self.server = None
        self.new_work = event.Event()

        # resources
        self.resources = []
        self.current_responses = OrderedDict()

        # environment
        self.env = Environment(loader=PackageLoader('monitor', 'templates'))

    def _set_log_handler(self, log_file):
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def run(self, config_file):
        with open(config_file, 'r') as yml_config:
            cfg = yaml.load(yml_config)

        if not cfg:
            raise InvalidConfigError(u'Config file is empty.')
        log_file = cfg.get('log_file')
        if not log_file:
            raise InvalidConfigError(u'Invalid config file. The "log_file" section is missing.')
        self._set_log_handler(log_file)

        sites = cfg.get('sites')
        if not sites:
            raise InvalidConfigError(u'Invalid config file. The "sites" section is missing.')
        for section in sites.itervalues():
            self.resources.append(MonitoredResource(section))

        self.scheduler = gevent.spawn(self._scheduler_job)
        self.supervisor = gevent.spawn(self._supervisor_job)
        self.server = gevent.spawn(self._server_job)

        gevent.joinall([self.scheduler, self.server])

    def _worker(self, resource):
        crawler = Crawler(resource)
        response = crawler.check()
        self.current_responses[resource] = response
        logger.info(response.message, extra=response.logger_info)

    def _supervisor_job(self):
        while True:
            for thread in list(self.pool):
                if thread.dead:
                    self.pool.discard(thread)
            try:
                job = self.workq.get_nowait()
            except queue.Empty:
                self.new_work.wait()
                self.new_work.clear()
                continue

            self.pool.spawn(self._worker, *job)

    def _scheduler_job(self):
        while True:
            for resource in self.resources:
                if resource.is_ready():
                    self.workq.put((resource, ))
                    self.new_work.set()

            gevent.sleep(60)

    def _server_job(self):
        WSGIServer(('', 8000), self._report_application).serve_forever()

    def _report_application(self, environ, start_response):
        status = '200 OK'
        template = self.env.get_template('report.html')
        body = template.render(responses=self.current_responses)

        headers = [
            ('Content-Type', 'text/html')
        ]
        start_response(status, headers)
        return [body.encode('utf-8')]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple program that monitors web sites "
                                                 "and reports their availability.")
    parser.add_argument("--config", dest="config_file", action="store", help="config file")
    args = parser.parse_args()

    monitor = Monitor()
    monitor.run(args.config_file)

