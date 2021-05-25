"""Provide some base configurations for tests."""
import os
import pytest
import py.path  # pyright: reportMissingModuleSource=false

from urllib.parse import urlparse, urlunparse

from p3exporter.collector import CollectorConfig

TEST_CASES_PATH = py.path.local(__file__).realpath() / '..' / 'test_cases'

def find_all_test_cases():
    """Generate list of test cases.

    :yield: generates each test case as list item
    :rtype: str
    """
    for c in TEST_CASES_PATH.listdir(sort=True):
        c = c.basename
        if c.endswith('.py'):
            yield c.replace('.py', '')


TEST_CASES = list(find_all_test_cases())


def cassette_name(test_name=None):
    """Generate cassette_name."""
    return 'tests/fixtures/{0}.yml'.format(test_name)


def get_case_name(path: str):
    return os.path.basename(os.path.splitext(path)[0])


def create_config(test_case: str, collector_opts: dict = None):
    """Create a valid configuration for given test case.

    This function creates a valid `CollectorConfig` object for a given test case.
    Extra `collector_opts` can be provided to configure the collector as needed.

    :param test_case: Name of the current test case for that a configuration has to be created.
    :type test_case: str
    :param collector_opts: Dictionary with optional extra options for given test case., defaults to {}
    :type collector_opts: dict, optional
    :return: A valid `CollectorConfig` object for the given test case.
    :rtype: CollectorConfig
    """
    cfg = dict(name=f"pythes for {test_case} collector", collectors=[test_case], collector_opts=dict(test_case=collector_opts))

    return CollectorConfig(**cfg)
