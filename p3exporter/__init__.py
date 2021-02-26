"""Init methods for p3exporter package"""
import argparse
from wsgiref.simple_server import make_server

import yaml
import logging
import signal
import sys
import time

from prometheus_client.core import REGISTRY

from p3exporter.collector import MyCollector, CollectorConfig
from p3exporter.web import create_app


def shutdown():
    """Function to shutdown the app in a clean way."""
    logging.info('Shutting down, see you next time!')
    sys.exit(1)


def signal_handler():
    """Function called if a signal was catched"""
    shutdown()


def main():
    """Main method to start the application"""
    signal.signal(signal.SIGTERM, signal_handler)

    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description="Python programmable Prometheus exporter.")
    parser.add_argument('-c', '--config-file', default='p3.yml',
                        help='path to configuration file.')
    parser.add_argument('-p', '--port', default=5876,
                        help='exporter exposed port')
    args = parser.parse_args()

    with open(args.config_file, 'r') as config_file:
        cfg = yaml.load(config_file, Loader=yaml.FullLoader)
    collector_config = CollectorConfig(**cfg)

    collector = MyCollector(collector_config)
    REGISTRY.register(collector)

    app = create_app(collector_config)

    logging.info("Start exporter, listen on {}".format(int(args.port)))
    httpd = make_server('', int(args.port), app)
    httpd.serve_forever()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        signal_handler()
