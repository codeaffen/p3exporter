"""Module that defines all needed classes and functions for example collector."""
import random
import time

from p3exporter.collector import CollectorBase, CollectorConfig
from p3exporter.cache import timed_lru_cache
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily


class ExampleCollector(CollectorBase):
    """A sample collector.

    It does not really do much. It only runs a method and return the time it runs as a gauge metric.
    """

    def __init__(self, config: CollectorConfig):
        """Instanciate a MyCollector object."""
        super(ExampleCollector, self).__init__(config)

    def collect(self):
        """Collect the metrics."""
        runtime, result = _run_process()
        yield GaugeMetricFamily('example_process_runtime', 'Time a process runs in seconds', value=runtime)
        yield InfoMetricFamily('example_process_status', 'Status of example process', value={'status': result})


@timed_lru_cache(10)
def _run_process():
    """Sample function to ran a command for metrics."""
    timer = time.perf_counter()
    time.sleep(random.random())  # nosec
    runtime = time.perf_counter() - timer
    return runtime, "sucess"
