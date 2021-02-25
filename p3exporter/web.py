from flask import Flask, render_template

from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from p3exporter import CollectorConfig


def create_app(config: CollectorConfig):

    app = Flask(__name__, instance_relative_config=True)

    @app.route("/")
    def index():
        return render_template("index.html", title=config.exporter_name)

    dispatched_app = DispatcherMiddleware(app, {
        '/metrics': make_wsgi_app()
    })

    return dispatched_app
