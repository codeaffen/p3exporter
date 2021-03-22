"""Entry point for collector sub module."""
import inflection
import logging

from importlib import import_module
from prometheus_client.core import REGISTRY


class CollectorConfig(object):
    """Class that provide all the logic needed for configuration handling."""

    def __init__(self, **kwargs):
        """Initialize instance variables.

        All configuration parameters are handed over as separate arguments.

        :raises Exception: Raises an exception if credentials are not well configured.
        """
        self.exporter_name = kwargs.pop('exporter_name', None)
        self.collectors = kwargs.pop('collectors', [])
        self.credentials = kwargs.pop('credentials', None)

        # do some fancy checks on configuration parameters
        if self.credentials is None:
            self.credentials = {}
        elif self.credentials is not None and (
                self.credentials['ssh_key'] is None or (
                    self.credentials['username'] is None or self.credentials['password'] is None)):
            raise Exception('Credential is not fully configured.')


class Collector(object):
    """Base class to load collectors.

    All collectors have to be placed inside the directory `collector`. You have to follow the naming convention:

    1. Place the collector code in a <name>.py file (e.g. `my.py`)
    2. Within the file <name>.py` a class <Name>Collector (e.g. `MyController`) needs to be defined.
       This is the main collector class which will be imported, instantiate and registered automatically.
    """

    def __init__(self, config: CollectorConfig):
        for c in config.collectors:
            try:
                collector_module = import_module("p3exporter.collector.{}".format(c), package=None)
                collector_class = getattr(collector_module, "{0}Collector".format(inflection.camelize(c)))
                collector = collector_class(config)
                REGISTRY.register(collector)
                logging.info("Collector '{0}' was loaded and registred sucessfully".format(c))
            except ModuleNotFoundError as e:
                logging.warning("Collector '{0}' not loaded: {1}".format(c, e.msg))
            except AttributeError as e:
                logging.warning("Collector '{0}' not loaded: {1}".format(c, e))
