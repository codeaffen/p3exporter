"""Entry point for collector sub module."""
import inflection
import logging
import re

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
        self.collector_opts = kwargs.pop('collector_opts', {})


class CollectorBase(object):
    """Base class for all collectors.

    This class will provide methods that do generic work.
    """

    def __init__(self, config: CollectorConfig):
        """Instantiate a CollectorBase object."""
        self.collector_name = self.collector_name_from_class
        self.opts = config.collector_opts.pop(self.collector_name, {})

    @property
    def collector_name_from_class(self):
        """Convert class name to controller name.

        The class name must follow naming convention:
            * camelized string
            * starts with camelized module name
            * ends with 'Collector'

        This will convert <Name>Collector class name to <name> collector name.
        Examples for valid names:
            * MyCollector => my
            * FooBarCollector => foo_bar
            * FooBarBazCollector => foo_bar_baz

        :return: collector name in snake case
        :rtype: string
        """
        class_name = re.sub(r'(?<=[a-z])[A-Z]|[A-Z](?=[^A-Z])', r'_\g<0>', self.__class__.__name__).lower().strip('_')
        class_name_parts = class_name.split('_')[0:-1]

        return '_'.join(class_name_parts)


class Collector(object):
    """Base class to load collectors.

    All collectors have to be placed inside the directory `collector`. You have to follow the naming convention:

    1. Place the collector code in a <name>.py file (e.g. `my.py`)
    2. Within the file <name>.py` a class <Name>Collector (e.g. `MyController`) needs to be defined.
       This is the main collector class which will be imported, instantiate and registered automatically.
    """

    def __init__(self, config: CollectorConfig):
        """Instantiate an CollectorBase object."""
        for c in config.collectors:
            try:
                collector_module = import_module("p3exporter.collector.{}".format(c), package=None)
                collector_class = getattr(collector_module, "{0}Collector".format(inflection.camelize(c)))
                collector = collector_class(config)
                REGISTRY.register(collector)
                logging.info("Collector '{0}' was loaded and registred successfully".format(c))
            except ModuleNotFoundError as e:
                logging.warning("Collector '{0}' not loaded: {1}".format(c, e.msg))
            except AttributeError as e:
                logging.warning("Collector '{0}' not loaded: {1}".format(c, e))
