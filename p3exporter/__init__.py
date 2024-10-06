"""Init methods for p3exporter package."""
import argparse
from wsgiref.simple_server import make_server

import yaml
import logging
import os
import signal
import sys
import time

from p3exporter.collector import Collector, CollectorConfig
from p3exporter.web import create_app


def setup_logging(cfg: dict):
    """Set up logging as configured.

    The configuration may optionally contain an entry `logging`,
    if it does not or if that entry is not an array then does nothing.
    Each array element must be a dict that contains at least a key
    `name` that refers to the logger to configure. It may also contain
    the optional keys `level` and `target` that configure the
    logging-level and a file-target, respectively if present.

    :param cfg: Configuration as read from config-file.
    :type cfg: dict
    """
    if not isinstance(cfg.get('logging'), list):
        return
    for c in cfg['logging']:
        if not isinstance(c, dict):
            return
        if not isinstance(c.get('name'), str):
            return
        logger = logging.getLogger(c["name"])
        level = c.get('level')
        if level is not None:
            logger.setLevel(level)
        target = c.get('target')
        if target is not None:
            logger.addHandler(logging.FileHandler(target))


def shutdown():
    """Shutdown the app in a clean way."""
    logging.info('Shutting down, see you next time!')
    sys.exit(1)


def signal_handler(signum, frame):
    """Will be called if a signal was catched."""
    shutdown()


def main():
    """Start the application."""
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Python programmable Prometheus exporter.")
    parser.add_argument('-c', '--config', default=os.getenv('P3E_CONFIG', 'p3.yml'),
                        help='path to configuration file.')
    parser.add_argument('-p', '--port', default=os.getenv('P3E_PORT', 5876),
                        help='exporter exposed port')
    args = parser.parse_args()

    with open(args.config, 'r') as config_file:
        cfg = yaml.load(config_file, Loader=yaml.SafeLoader)
    collector_config = CollectorConfig(**cfg)
    setup_logging(cfg)

    Collector(collector_config)

    app = create_app(collector_config)

    logging.info("Start exporter, listen on {}".format(int(args.port)))
    httpd = make_server('', int(args.port), app)
    httpd.serve_forever()

    while True:
        time.sleep(5)
