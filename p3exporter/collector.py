import random
import time

from prometheus_client.core import GaugeMetricFamily


class CollectorConfig(object):
    def __init__(self, **kwargs):

        self.exporter_name = kwargs.pop('exporter_name', None)
        self.credentials = kwargs.pop('credentials', None)

        # do some fancy checks on configuration parameters
        if self.credentials is None:
            self.credentials = {}
        elif self.credentials is not None and (
                self.credentials['ssh_key'] is None or (
                    self.credentials['username'] is None or self.credentials['password'] is None)):
            raise Exception('Credential is not fully configured.')


class MyCollector(object):
    def __init__(self, config: CollectorConfig):
        pass

    def collect(self):
        timer = time.perf_counter()
        self._run_process()
        timer = time.perf_counter() - timer
        yield GaugeMetricFamily('my_process_runtime', 'Time a process runs in seconds', value=timer)

    def _run_process(self):
        time.sleep(random.random())
