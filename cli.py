import pickle
from blueprints.tracing.documents import Location, Customer
from flask import Flask
import click


def register_commands(app: Flask):
    @app.cli.command("dump")
    @click.argument("key")
    def dump(key):
        """Dump all customers into a json"""
        location = Location.objects(key=key).first()
        if location is None:
            return {"description": "Location not found"}

        customers = [
            {
                "name": customer.name,
                "phone_number": customer.phone_number,
                "location": location.name,
                "time_in": customer.time_in,
            }
            for customer in Customer.objects(location=location.name)
        ]
        customer_obj = {"key": location.public_key, "customers": customers}
        with open("scripts/dumps/dumps.pickle", "wb+") as handle:
            pickle.dump(customer_obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
