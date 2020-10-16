import secrets

from flask_apispec import doc, use_kwargs, marshal_with
from flask_marshmallow import Schema
from webargs import fields
from flask import send_file

import config
from .tracing_base_resource import TracingBaseResource
from ..documents import Location
from ..documents.customer import Customer
import pickle


class LocationsResource(TracingBaseResource):
    class PostLocationSchema(Schema):
        name = fields.Str(description="Location name", example="Sweet Turtle Dessert", required=True)
        public_key = fields.Str(description="Public key used to encode data", required=True)
        api_key = fields.Str(description="API key to create a new location.")

    class LocationSchema(Schema):
        key = fields.Str(description="Key used to pass in customer information")

    @doc(description="Create a new location, and generate a private key that will only be shown once.")
    @use_kwargs(PostLocationSchema)
    @marshal_with(LocationSchema)
    def post(self, **kwargs):
        if not secrets.compare_digest(kwargs["api_key"], config.API_KEY):
            return {"description": "Invalid API key"}

        location = Location.create(name=kwargs["name"], public_key=kwargs['public_key'])

        return {
            "key": location.key,
        }


class LocationResource(TracingBaseResource):
    class PostCustomerSchema(Schema):
        key = fields.Str(description="Location's key")
        name = fields.Str(description="Customer's full name", example="John Doe")
        phone_number = fields.Str(description="Customer's contact phone number", example="+16471231234")

    class ReturnCustomerSchema(Schema):
        time_in = fields.Str(description="The time that the customer created the entry")

    class DumpCustomersSchema(Schema):
        name = fields.Str(description='name of restaurant')

    @doc(description="Create a new customer associated with a location, encrypting it into the database.")
    @use_kwargs(PostCustomerSchema)
    @marshal_with(ReturnCustomerSchema)
    def post(self, **kwargs):
        # search for location, return 404 if not found
        location = Location.objects(key=kwargs["key"]).first()
        if location is None:
            return {"description": "Location not found"}

        customer = Customer.create(
            location=location,
            name=kwargs["name"],
            phone_number=kwargs["phone_number"],
        )

        return {
            "time_in": customer.time_in
        }

    @use_kwargs(DumpCustomersSchema)
    def get(self, name):
        """Dump all customers into a json"""
        location = Location.objects(name=name).first()
        if location is None:
            return {"description": "Location not found"}

        customers = [
            {
                'name': customer.name,
                'phone_number': customer.phone_number,
                'location': location.name,
                'time_in': customer.time_in
            }
            for customer in Customer.objects(location=location.name)
        ]
        with open('dumps.pickle', 'wb') as handle:
            pickle.dump(customers, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return send_file('dumps.pickle', as_attachment=True)
