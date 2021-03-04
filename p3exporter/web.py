"""Web module provide all parts to create the web app."""
from flask import Flask, render_template

from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from p3exporter import CollectorConfig


def create_app(config: CollectorConfig):
    """Create the web app.

    This Function creates the flask app and dispatch metrics endpoint to prometheus wsgi app.

    :param config: A configuration object with data for template rendering.
    :type config: CollectorConfig
    :return: Created web app object.
    :rtype: DispatcherMiddleware
    """
    app = Flask(__name__, instance_relative_config=True)

    @app.route("/")
    def index(): # pylint: disable=W0612
        return render_template("index.html", title=config.exporter_name)

    dispatched_app = DispatcherMiddleware(app, {
        '/metrics': make_wsgi_app()
    })

    return dispatched_app
