"""Application API."""

from flask import Blueprint
from flask_restx import Api  # type: ignore

from configmodel.api.namespaces.hello import api as ns_hello

blueprint = Blueprint("api", __name__)

api = Api(blueprint)

api.add_namespace(ns_hello)
