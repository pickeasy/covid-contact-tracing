import os

import mongoengine
import sentry_sdk
from flask import Flask, jsonify
from flask_apispec import FlaskApiSpec
from flask_cors import CORS
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.redis import RedisIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

import config as c
import loggers
from extensions import logger
from spec import APISPEC_SPEC

project_dir = os.path.dirname(os.path.abspath(__file__))


def create_app(testing=False):
    """ Application Factory. """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(c)
    app.config["TESTING"] = testing

    # cors
    CORS(
        app, expose_headers=["Authorization"], resources={"/*": {"origins": c.ORIGINS}}
    )

    app.before_request(loggers.before_request)

    register_extensions(testing)
    register_blueprints(app)
    register_shell(app)
    register_external()

    # Return validation errors as JSON
    @app.errorhandler(422)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages}), err.code, headers
        else:
            return jsonify({"errors": messages}), err.code

    @app.errorhandler(404)
    def handle_404(err):
        return jsonify({"description": "Not Found"}), err.code

    return app


def register_shell(app: Flask):
    """ Expose more attributes to the Flask Shell. """

    @app.shell_context_processor
    def make_shell_context():
        # make below variables accessible in the shell for testing purposes
        return {"app": app}


def register_extensions(testing: bool):
    """ Register Flask extensions. """

    url = c.MONGODB_URL if not testing else c.TEST_MONGODB_URL
    mongoengine.connect(host=url, tz_aware=True)


def register_blueprints(app: Flask):
    """ Register Flask blueprints. """
    app.config.update({"APISPEC_SPEC": APISPEC_SPEC})
    docs = FlaskApiSpec(app)

    # example blueprint
    from blueprints.tracing import tracing_bp
    from blueprints.tracing import routes as example_routes

    example_routes.set_routes(app, tracing_bp, docs)


def register_external():
    """ Register external integrations. """
    # sentry
    if len(c.SENTRY_DSN) == 0:
        logger.warning("Sentry DSN not set.")
    else:
        sentry_sdk.init(
            c.SENTRY_DSN,
            integrations=[
                FlaskIntegration(),
                RedisIntegration(),
                SqlalchemyIntegration(),
            ],
        )
