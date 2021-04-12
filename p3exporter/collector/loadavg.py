"""Module that defines all needed classes and functions for loadavg collector."""
import os

from p3exporter.collector import CollectorBase, CollectorConfig
from prometheus_client.core import GaugeMetricFamily


class LoadavgCollector(CollectorBase):
    """Load avg collector class."""

    def __init__(self, config: CollectorConfig):
        """Instanciate a CpuCollector object."""
        super(LoadavgCollector, self).__init__(config)

    def collect(self):
        """Collect load avg for 1, 5 and 15 minutes interval.

        Returns three gauge metrics. One for each load.
        """
        self.avg1, self.avg5, self.avg15 = os.getloadavg()
        yield GaugeMetricFamily('load_avg_1', "1m load average.", value=self.avg1)
        yield GaugeMetricFamily('load_avg_5', "5m load average.", value=self.avg5)
        yield GaugeMetricFamily('load_avg_15', "15m load average.", value=self.avg15)
