from __future__ import annotations

import secrets

from mongoengine import Document, StringField


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
    def create(cls, name, public_key) -> Location:
        key = secrets.token_hex(48)

        location = cls(name=name, public_key=public_key, key=key).save()

        return location
