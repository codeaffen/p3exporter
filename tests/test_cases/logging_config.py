from p3exporter import setup_logging
from p3exporter.collector import CollectorBase, CollectorConfig
import logging
import os.path
import pytest


loggers = ["", "foo", "bar"]
files = ["file1.log", "file2.log"]


def setup_function(fn):
    """Start with a clean slate of default logging-levels and no handlers."""
    for name in loggers:
        logger = logging.getLogger(name)
        level = logging.WARNING if name == "" else logging.NOTSET
        logger.setLevel(level)
        for handler in logger.handlers:
            logger.removeHandler(handler)


def teardown_function(fn):
    """Remove any files we may have created."""
    for file in files:
        if os.path.exists(file):
            os.remove(file)


data_logging_levels = [
    pytest.param(None,
                 [logging.WARNING, logging.NOTSET, logging.NOTSET],
                 [None, None, None],
                 id="no logging-section at all"),
    pytest.param("Not an array",
                 [logging.WARNING, logging.NOTSET, logging.NOTSET],
                 [None, None, None],
                 id="logging-section has wrong type"),
    pytest.param([{"level": "INFO"},
                  {"target": "file1.log"},
                  {"level": "DEBUG", "target": "file2.log"}],
                 [logging.WARNING, logging.NOTSET, logging.NOTSET],
                 [None, None, None],
                 id="no names in otherwise valid entries"),
    pytest.param([{"name": "", "level": "INFO"},
                  {"name": "foo", "level": "DEBUG"}],
                 [logging.INFO, logging.DEBUG, logging.NOTSET],
                 [None, None, None],
                 id="levels only, using empty-string for root"),
    pytest.param([{"name": "root", "level": "ERROR"},
                  {"name": "bar", "level": "CRITICAL"}],
                 [logging.ERROR, logging.NOTSET, logging.CRITICAL],
                 [None, None, None],
                 id="levels only, using name of root"),
    pytest.param([{"name": "foo", "level": 10},
                  {"name": "bar", "level": 20}],
                 [logging.WARNING, logging.DEBUG, logging.INFO],
                 [None, None, None],
                 id="levels only, using integers for levels"),
    pytest.param([{"name": "root", "target": "file1.log"},
                  {"name": "foo", "target": "file2.log"}],
                 [logging.WARNING, logging.NOTSET, logging.NOTSET],
                 ["file1.log", "file2.log", None],
                 id="targets only"),
    pytest.param([{"name": "foo", "level": "INFO", "target": "file1.log"}],
                 [logging.WARNING, logging.INFO, logging.NOTSET],
                 [None, "file1.log", None],
                 id="both level and target"),
    ]


@pytest.mark.parametrize("cfg_logging,levels,targets", data_logging_levels)
def test_logging_levels(cfg_logging, levels, targets):
    # pytest adds lots of extra handlers, so remember the starting state
    orig_handlers = []
    for name in loggers:
        logger = logging.getLogger(name)
        orig_handlers.append(logger.handlers.copy())

    # GIVEN an input config-dictionary
    cfg = {
        "exporter_name": "Test only",
        "collectors": [],
        "collector_opts": {},
    }
    if cfg_logging is not None:
        cfg["logging"] = cfg_logging

    # WHEN calling setup_logging()
    setup_logging(cfg)

    # THEN the logging-levels should get changed to the expected
    for i, name in enumerate(loggers):
        logger = logging.getLogger(name)
        assert logger.level == levels[i]

    # AND the expected file-handlers should get added
    for i, name in enumerate(loggers):
        logger = logging.getLogger(name)
        added_handlers = [h for h in logger.handlers
                          if h not in orig_handlers[i]]
        if targets[i] is None:
            assert len(added_handlers) == 0
        else:
            assert len(added_handlers) == 1
            handler = added_handlers[0]
            assert isinstance(handler, logging.FileHandler)
            assert handler.baseFilename == os.path.abspath(targets[i])


class FooCollector(CollectorBase):
    pass


data_collectorbase_setloggers = [
    pytest.param(None,
                 ["foo", "bar"],
                 [logging.WARNING, logging.NOTSET, logging.NOTSET],
                 id="no log_level setting"),
    pytest.param("CRITICAL",
                 "foo",
                 [logging.WARNING, logging.CRITICAL, logging.NOTSET],
                 id="single logger-name"),
    pytest.param("ERROR",
                 ["foo", "bar"],
                 [logging.WARNING, logging.ERROR, logging.ERROR],
                 id="list of loggers"),
    pytest.param(20,
                 ["", "foo"],
                 [logging.INFO, logging.INFO, logging.NOTSET],
                 id="numeric log_level"),
    ]


@pytest.mark.parametrize("cfg_log_level,logger_names,expected",
                         data_collectorbase_setloggers)
def test_collectorbase_setloggers(cfg_log_level, logger_names, expected):
    # GIVEN an input config-dictionary
    cfg = {
        "exporter_name": "Test only",
        "collectors": ["foo"],
        "collector_opts": {
            "foo": {}
        },
    }
    if cfg_log_level is not None:
        cfg["collector_opts"]["foo"]["log_level"] = cfg_log_level

    # AND a collector-base using this config
    collector = FooCollector(CollectorConfig(**cfg))

    # WHEN the setLoggers() method is called
    collector.setLoggers(logger_names)

    # THEN the logging-levels should get changed to the expected
    for i, name in enumerate(loggers):
        logger = logging.getLogger(name)
        assert logger.level == expected[i]
