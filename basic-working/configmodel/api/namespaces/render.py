"""Render namespace."""

from flask_restx import Namespace, Resource, fields, reqparse  # type: ignore

from configmodel.logic.config import get_config
from configmodel.logic.service import get_service
from configmodel.templates.render import render

api = Namespace("render", description="Render operations")

render_parser = reqparse.RequestParser()
render_parser.add_argument("family", type=str, help="Vendor family", required=True)

render_model = api.model(
    "Render",
    {
        "hostname": fields.String(required=True, description="Device hostname"),
        "config": fields.String(required=True, description="Configuration text"),
    },
)


@api.route("/config/<int:config_id>")
@api.response(404, "config_id not found")
@api.expect(render_parser, validate=True)
class ConfigRender(Resource):
    """Render a single config item."""

    @api.marshal_with(render_model)
    def get(self, config_id):
        """Render a given config."""
        args = render_parser.parse_args()
        config = get_config(config_id)
        if config is None:
            api.abort(404)
        ret = {
            "hostname": config.hostname,
            "config": render(args["family"], config.schema, config.config),
        }
        return ret


@api.route("/service/<int:service_id>")
@api.response(404, "service_id not found")
@api.expect(render_parser, validate=True)
class ServiceRender(Resource):
    """Render a single service item."""

    @api.marshal_list_with(render_model)
    def get(self, service_id):
        """Render a given service."""
        args = render_parser.parse_args()
        service = get_service(service_id)
        if service is None:
            api.abort(404)

        return_list = []
        for hostname, configs in service["config"].items():
            return_config = []
            for schema, config in configs.items():
                return_config.append(render(args["family"], schema, config))
            return_list.append(
                {"hostname": hostname, "config": "!\n".join(return_config)}
            )
        return return_list
