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

    def setLoggers(self, logger_names: list | str):
        """Configure the provided logger(s) according to the CollectorConfig.

        It is recommended to call this method from the constructor of any
        deriving class. Either bump the required p3exporter version or check
        dynamically if the method is supported.

        :param logger_names: Name or names of loggers to configure.
        :type logger_names: list or str
        """
        if not isinstance(logger_names, list):
            logger_names = [logger_names]
        if "log_level" not in self.opts:
            return
        level = self.opts["log_level"]
        for name in logger_names:
            logger = logging.getLogger(name)
            logger.setLevel(level)


class Collector(object):
    """Base class to load collectors.

    Collectors needs to be placed either in the directory `collector` within this module (local) or in a separate module.
    Collectors in separate modules needs to be addressed in dotted notation.

    Collectors have to follow the following naming convention:

    1. Place the collector code in a <name>.py file (e.g. `my.py`)
    2. Within the file <name>.py` a class <Name>Collector (e.g. `MyController`) needs to be defined.
       This is the main collector class which will be imported, instantiate and registered automatically.
    """

    def __init__(self, config: CollectorConfig):
        """Instantiate an CollectorBase object."""
        _collectors = [c if "." in c else "p3exporter.collector.{}".format(c) for c in config.collectors]
        for c in _collectors:
            try:
                collector_module = import_module(c, package=None)
                collector_class = getattr(collector_module, "{0}Collector".format(inflection.camelize(c.split('.')[-1])))
                collector = collector_class(config)
                REGISTRY.register(collector)
                logging.info("Collector '{0}' was loaded and registred successfully".format(c))
            except ModuleNotFoundError as e:
                logging.warning("Collector '{0}' not loaded: {1}".format(c, e.msg))
            except AttributeError as e:
                logging.warning("Collector '{0}' not loaded: {1}".format(c, e))
