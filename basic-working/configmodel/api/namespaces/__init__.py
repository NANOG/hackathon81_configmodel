"""Application API."""

from flask import Blueprint
from flask_restx import Api  # type: ignore

from configmodel.api.namespaces.config import api as ns_config
from configmodel.api.namespaces.render import api as ns_render
from configmodel.api.namespaces.service import api as ns_service

blueprint = Blueprint("api", __name__)

api = Api(blueprint)

api.add_namespace(ns_config)
api.add_namespace(ns_render)
api.add_namespace(ns_service)
