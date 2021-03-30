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
        self.timer = time.perf_counter()
        i_labels = {'status': _run_process()}
        runtime = time.perf_counter() - self.timer
        yield GaugeMetricFamily('example_process_runtime', 'Time a process runs in seconds', value=runtime)
        i = InfoMetricFamily('example_process_status', 'Status of example process', labels=i_labels.keys())
        i.add_metric(labels=i_labels.keys(), value=i_labels)
        yield i


@timed_lru_cache(10)
def _run_process():
    """Sample function to ran a command for metrics."""
    time.sleep(random.random()) # nosec
    return "sucess"
