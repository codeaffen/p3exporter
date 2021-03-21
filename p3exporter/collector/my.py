import random
import time

from p3exporter.collector import CollectorConfig
from prometheus_client.core import GaugeMetricFamily

class MyCollector(object):
    """A sample collector.

    It does not really do much. It only runs a method and return the time it runs as a gauge metric.
    """

    def __init__(self, config: CollectorConfig):
        """Instanciate a MyCollector object."""
        pass

    def collect(self):
        """Collect the metrics."""
        self.timer = time.perf_counter()
        _run_process()
        runtime = time.perf_counter() - self.timer
        yield GaugeMetricFamily('my_process_runtime', 'Time a process runs in seconds', value=runtime)

def _run_process():
    """Sample function to ran a command for metrics."""
    time.sleep(random.random()) # nosec
