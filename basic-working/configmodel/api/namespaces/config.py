"""Config namespace."""

from flask_restx import Namespace, Resource, fields  # type: ignore

from jsonschema import ValidationError  # type: ignore

from configmodel.logic.config import (
    create_config,
    delete_config,
    get_config,
    get_configs,
    validate_config,
)


api = Namespace("config", description="Config operations")

config_model = api.model(
    "Config",
    {
        "config_id": fields.Integer(
            readonly=True, description="The configuration unique identifier"
        ),
        "hostname": fields.String(required=True, description="Device hostname"),
        "schema": fields.String(required=True, description="Configuration schema name"),
        "config": fields.Raw(required=True, description="Configuration JSON object"),
    },
)


@api.route("/")
class ConfigList(Resource):
    """Shows a list of all configs, and lets you POST to add new ones."""

    @api.marshal_list_with(config_model)
    def get(self):
        """List all configs."""
        return get_configs()

    @api.expect(config_model, validate=True)
    @api.marshal_with(config_model, code=201, mask=None)
    def post(self):
        """Create a new config."""
        try:
            validate_config(api.payload)
        except ValidationError as e:
            api.abort(400, e)
        config = create_config(
            hostname=api.payload["hostname"],
            schema=api.payload["schema"],
            config=api.payload["config"],
        )

        return config, 201


@api.route("/<int:config_id>")
@api.response(404, "config_id not found")
@api.param("config_id", "The config identifier")
class Config(Resource):
    """Show a single config item and lets you delete it."""

    @api.marshal_with(config_model)
    def get(self, config_id):
        """Fetch a given config."""
        config = get_config(config_id)
        if config is None:
            api.abort(404)
        return config

    @api.response(204, "Config deleted")
    def delete(self, config_id):
        """Delete a config given its identifier."""
        result = delete_config(config_id)
        if not result:
            api.abort(404)
        return "", 204
