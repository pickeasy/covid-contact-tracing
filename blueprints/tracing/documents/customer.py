from __future__ import annotations

from datetime import datetime, timezone

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from mongoengine import Document, DateTimeField, ReferenceField, BinaryField

from blueprints.tracing.documents import Location


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
    meta = {
        'indexes': [
            {'fields': ['time_in'], 'expireAfterSeconds': 2592000}
        ]
    }

    @classmethod
    def create(cls, name: str, phone_number: str, location: Location) -> Customer:
        public_key = RSA.import_key(location.public_key)
        cipher = PKCS1_OAEP.new(key=public_key)

        encrypted_name = cipher.encrypt(name.encode("utf-8"))
        encrypted_phone = cipher.encrypt(phone_number.encode("utf-8"))

        customer = cls(
            name=encrypted_name,
            phone_number=encrypted_phone,
            time_in=datetime.utcnow().replace(tzinfo=timezone.utc)
        )

        customer.location = location
        customer.save()
        return customer

    def decrypt(self, private_key_str: str) -> dict:
        """
        Return a decrypted version of the customer.
        """
        private_key = RSA.import_key(private_key_str)
        cipher = PKCS1_OAEP.new(key=private_key)

        decrypted_name = cipher.decrypt(self.name)
        decrypted_phone_number = cipher.decrypt(self.phone_number)

        return {
            "name": decrypted_name,
            "phone_number": decrypted_phone_number,
            "time_in": self.time_in
        }
