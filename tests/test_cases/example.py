import re

from tests.conftest import get_case_name, create_config
from p3exporter.collector.example import ExampleCollector


test_case = get_case_name(__file__)
collector_config = create_config(test_case)


def test_expected_metrics():
    collector = ExampleCollector(collector_config)
    metric = next(collector.collect())

    assert re.search(r'(?<=value=)\d+\.\d+', str(metric))
