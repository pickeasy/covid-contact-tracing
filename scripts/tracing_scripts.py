from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json
import pickle
from blueprints.tracing.documents import Location, Customer
from mongoengine import connect

url = "mongodb://pickeasy:pickeasy@localhost:27018/menus?authSource=admin"
connect(host=url, tz_aware=True)


def generate_key_values(slug):
    """ Generates key value pairs of public and private keys"""
    with open("keys.json", "r") as f:
        keys = json.load(f)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b"pickeasy-tracing"),
    ).decode("utf-8")
    public_key = (
        key.public_key()
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode("utf-8")
    )
    keys[public_key] = private_key
    location = Location.create(slug=slug, public_key=public_key)
    location.save()
    print(f"Your key\n{location.key}\n")
    with open("keys.json", "w") as f:
        json.dump(keys, f)


def decrypt(slug: str):
    """take dump of encrypted customer data of return json file decrypted"""

    location = Location.objects(slug=slug).first()
    if location is None:
        return "Location not found"

    customers = [
        {
            "name": customer.name,
            "phone_number": customer.phone_number,
            "location": location.slug,
            "time_in": customer.time_in,
        }
        for customer in Customer.objects(location=slug)
    ]
    customer_obj = {"key": location.public_key, "customers": customers}
    with open("../scripts/dumps/dumps.pickle", "wb+") as handle:
        pickle.dump(customer_obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open("keys.json", "r") as f:
        keys = json.load(f)
    with open("dumps/dumps.pickle", "rb") as handle:
        encrypted_customers = pickle.load(handle)
    private_key = keys[encrypted_customers["key"]]
    key = serialization.load_pem_private_key(
        private_key.encode("utf-8"), password=b"pickeasy-tracing"
    )
    decrypted_customers = []
    for customer in encrypted_customers["customers"]:
        decrypted_name = (
            key.decrypt(
                customer["name"],
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            .decode("utf-8")
            .split("|")[0]
        )
        decrypted_phone_number = (
            key.decrypt(
                customer["phone_number"],
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            .decode("utf-8")
            .split("|")[0]
        )
        customer["time_in"] = str(customer["time_in"])
        customer["name"] = decrypted_name
        customer["phone_number"] = decrypted_phone_number
        decrypted_customers.append(customer)
    with open("out/out.json", "w+") as out:
        json.dump({"customers": decrypted_customers}, out)


def prompt():
    option = input(
        "Enter 1 to create a new key for a restaurant, 2 to decode customer data and 3 to exit script\n"
    )
    if option == "1":
        slug = input("Enter location name\n")
        generate_key_values(slug)
        prompt()
    elif option == "2":
        slug = input("Enter target location name\n")
        decrypt(slug)
        print("Your data is in out/out.json\n")
        prompt()
    elif option == "3":
        print("Exit by user\n")
        exit()
    else:
        prompt()


if __name__ == "__main__":
    prompt()
