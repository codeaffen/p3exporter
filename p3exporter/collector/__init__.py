import random
import time

from prometheus_client.core import GaugeMetricFamily


class CollectorConfig(object):
    """Class that provide all the logic needed for configuration handling."""
    def __init__(self, **kwargs):
        """Initialize instance variables.

        All configuration parameters are handed over as separate arguments.

        :raises Exception: Raises an exception if credentials are not well configured.
        """
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
    """A sample collector.

    It does not really do much. It only runs a method and return the time it runs as a gauge metric.
    """
    def __init__(self, config: CollectorConfig):
        pass

    def collect(self):
        """Function that collects the metrics"""
        timer = time.perf_counter()
        self._run_process()
        timer = time.perf_counter() - timer
        yield GaugeMetricFamily('my_process_runtime', 'Time a process runs in seconds', value=timer)

    def _run_process(self):
        """Sample fuction to ran a command for metrics"""
        time.sleep(random.random())