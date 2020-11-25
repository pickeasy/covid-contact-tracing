import secrets

from flask_apispec import doc, use_kwargs, marshal_with
from flask_marshmallow import Schema
from webargs import fields

import config
from .tracing_base_resource import TracingBaseResource
from ..documents import Location
from ..documents.customer import Customer


class LocationResource(TracingBaseResource):
    class PostCustomerSchema(Schema):
        key = fields.Str(description="Location's key")
        name = fields.Str(description="Customer's full name", example="John Doe")
        phone_number = fields.Str(
            description="Customer's contact phone number", example="+16471231234"
        )

    class ReturnCustomerSchema(Schema):
        time_in = fields.Str(description="The time that the customer created the entry")

    @doc(
        description="Create a new customer associated with a location, encrypting it into the database."
    )
    @use_kwargs(PostCustomerSchema)
    @marshal_with(ReturnCustomerSchema)
    def post(self, name, **kwargs):
        # search for location, return 404 if not found
        location = Location.objects(name=name, key=kwargs["key"]).first()
        if location is None:
            return {"description": "Location not found"}

        customer = Customer.create(
            location=location, name=kwargs["name"], phone_number=kwargs["phone_number"],
        )

        return {"time_in": customer.time_in}
