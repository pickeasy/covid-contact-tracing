from __future__ import annotations

import secrets
from typing import Tuple

from mongoengine import Document, StringField

from Crypto.PublicKey import RSA


class Location(Document):

    name = StringField(primary_key=True)
    """
    Name of location for identification purposes.
    """

    public_key = StringField(required=True)
    """
    Public key is used to encrypt the data into the database.
    """

    key = StringField(required=True)
    """
    A key that is used to authenticate customer's contact tracing information.
    """

    @classmethod
    def create(cls, name) -> Tuple[Location, str]:
        private_key = RSA.generate(2048)
        public_key = private_key.publickey()
        private_pem = private_key.export_key().decode()
        public_pem = public_key.export_key().decode()

        key = secrets.token_hex(48)

        location = cls(name=name, public_key=public_pem, key=key).save()

        return location, private_pem
