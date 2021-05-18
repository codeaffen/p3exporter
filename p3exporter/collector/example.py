"""Module that defines all needed classes and functions for example collector."""
import asyncio
import random
import time

from p3exporter.collector import CollectorBase, CollectorConfig
from p3exporter.cache import timed_lru_cache, timed_async_lru_cache
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
        cached_runtime, cached_result = _run_process_cache_results()
        yield GaugeMetricFamily('example_cached_process_runtime', 'Time a process runs in seconds', value=cached_runtime)
        yield InfoMetricFamily('example_cached_process_status', 'Status of example process', value={'status': cached_result})
        async_runtime, async_result = asyncio.run(_run_async_process_cache_results())
        yield GaugeMetricFamily('example_cached_async_process_runtime', 'Time a process runs in seconds', value=async_runtime)
        yield InfoMetricFamily('example_cached_async_process_status', 'Status of example process', value={'status': async_result})


def _run_process():
    """Sample function to ran a command for metrics."""
    timer = time.perf_counter()
    time.sleep(random.random())  # nosec
    runtime = time.perf_counter() - timer
    return runtime, "success"

@timed_lru_cache(10)
def _run_process_cache_results():
    """Sample function to ran a command for metrics."""
    timer = time.perf_counter()
    time.sleep(random.random())  # nosec
    runtime = time.perf_counter() - timer
    return runtime, "success"

@timed_async_lru_cache(10)
async def _run_async_process_cache_results():
    """Sample function to ran a command for metrics."""
    timer = time.perf_counter()
    time.sleep(30 + random.random())  # nosec
    runtime = time.perf_counter() - timer
    return runtime, "success"
