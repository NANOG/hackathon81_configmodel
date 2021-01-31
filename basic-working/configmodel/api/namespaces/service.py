"""Service namespace."""

from flask_restx import Namespace, Resource, fields  # type: ignore

from jsonschema import ValidationError  # type: ignore

from configmodel.logic.service import (
    create_service,
    delete_service,
    get_service,
    get_services,
    validate_service,
)


api = Namespace("service", description="Service operations")

service_model = api.model(
    "Service",
    {
        "service_id": fields.Integer(
            readonly=True, description="Service unique identifier"
        ),
        "schema": fields.String(required=True, description="Service schema name"),
        "config": fields.Raw(
            required=True, description="Service definition JSON object"
        ),
    },
)


@api.route("/")
class ServiceList(Resource):
    """Shows a list of all services, and lets you POST to add new ones."""

    @api.marshal_list_with(service_model)
    def get(self):
        """List all services."""
        return get_services()

    @api.expect(service_model, validate=True)
    @api.marshal_with(service_model, code=201, mask=None)
    def post(self):
        """Create a new service."""
        # verify payload (configs)
        try:
            validate_service(api.payload)
        except ValidationError as e:
            api.abort(400, e)

        # create configs and service
        try:
            service = create_service(api.payload)
        except Exception as e:
            api.abort(400, e)

        api.payload["service_id"] = service.service_id

        return api.payload, 201


@api.route("/<int:service_id>")
@api.response(404, "service_id not found")
@api.param("service_id", "The service identifier")
class Service(Resource):
    """Show a single service item and lets you delete it."""

    @api.marshal_with(service_model)
    def get(self, service_id):
        """Fetch a given service."""
        service = get_service(service_id)
        if service is None:
            api.abort(404)
        return service

    @api.response(204, "Service deleted")
    def delete(self, service_id):
        """Delete a service given its identifier."""
        result = delete_service(service_id)
        if not result:
            api.abort(404)
        return "", 204
