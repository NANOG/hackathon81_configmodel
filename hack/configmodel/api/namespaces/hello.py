"""Hello namespace."""

from flask_restx import Namespace, Resource, fields, reqparse  # type: ignore

api = Namespace("hello", description="Hello!")

hello_model = api.model(
    "Hello",
    {
        "message": fields.String(required=True, description="Our hello message"),
    },
)

hello_parser = reqparse.RequestParser()
hello_parser.add_argument(
    "name", type=str, help="Person to say hello to", required=False
)


@api.route("/")
class Hello(Resource):
    """Our hellos."""

    @api.marshal_with(hello_model, mask=None)
    @api.expect(hello_parser)
    def get(self):
        """Say hello."""
        args = hello_parser.parse_args()
        if args["name"]:
            return {"message": "hello {}!".format(args["name"])}

        return {"message": "hello!"}
