from flask import Blueprint, Flask
from flask_apispec import FlaskApiSpec

from . import bp_name
from .controllers import (
    LocationsResource,
    LocationResource,
)


def set_routes(app: Flask, bp: Blueprint, docs: FlaskApiSpec):
    # a list of resources
    resources = [
        (LocationsResource, "/locations", "locations", ["POST"]),
        (LocationResource, "/locations/<string:name>", "dumps", ['GET']),
        (LocationResource, "/locations/<string:name>/customers", "customers", ["POST"]),
    ]

    for resource, route, name, methods in resources:
        bp.add_url_rule(route, view_func=resource.as_view(name), methods=methods)

    app.register_blueprint(bp)

    for resource, route, name, methods in resources:
        docs.register(resource, blueprint=bp_name, endpoint=name)
