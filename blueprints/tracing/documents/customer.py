from __future__ import annotations

from datetime import datetime, timezone

from mongoengine import Document, DateTimeField, ReferenceField, BinaryField

from blueprints.tracing.documents import Location

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import secrets


class Customer(Document):
    name = BinaryField(required=True)
    """
    Encrypted name based on location's public key.
    """

    phone_number = BinaryField(required=True)
    """
    Encrypted phone_number based on location's public key.
    """

    time_in = DateTimeField(default=datetime.utcnow, required=True)
    """
    The time that the customer registers their information.
    """

    location = ReferenceField(Location)

    # regulations state that we must destroy the information 30 days after
    # visiting.
    meta = {"indexes": [{"fields": ["time_in"], "expireAfterSeconds": 2592000}]}

    @classmethod
    def create(cls, name: str, phone_number: str, location: Location) -> Customer:
        public_key = serialization.load_pem_public_key(
            location.public_key.encode("utf-8")
        )
        secret_name = name + '|' + secrets.token_hex(48)
        encrypted_name = public_key.encrypt(
            secret_name.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        secret_phone_number = phone_number + '|' + secrets.token_hex(48)
        encrypted_phone = public_key.encrypt(
            secret_phone_number.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        customer = cls(
            name=encrypted_name,
            phone_number=encrypted_phone,
            time_in=datetime.utcnow().replace(tzinfo=timezone.utc),
        )

        customer.location = location
        customer.save()
        return customer
