from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import json
import pickle


def generate_key_values(name):
    """ Generates key value pairs of public and private keys"""
    with open("keys.json", "r") as f:
        keys = json.load(f)
    f.close()
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
    keys[name] = private_key
    f = open("out/public_key.txt", "w")
    f.write(public_key)
    f.close()
    with open("keys.json", "w") as f_json:
        json.dump(keys, f_json)
    f_json.close()


def decrypt():
    """take dump of encrypted customer data of return json file decrypted"""
    with open("keys.json", "r") as f:
        keys = json.load(f)
    with open("dumps/dumps.pickle", "rb") as handle:
        encrypted_customers = pickle.load(handle)
    decrypted_customers = []
    for customer in encrypted_customers:
        private_key = keys[customer["location"]]
        key = serialization.load_pem_private_key(
            private_key.encode("utf-8"), password=b"pickeasy-tracing"
        )
        decrypted_name = key.decrypt(
            customer["name"],
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        ).decode("utf-8")
        decrypted_phone_number = key.decrypt(
            customer["phone_number"],
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        ).decode("utf-8")
        customer["time_in"] = str(customer["time_in"])
        customer["name"] = decrypted_name
        customer["phone_number"] = decrypted_phone_number
        decrypted_customers.append(customer)
    with open("out/out.json", "w") as out:
        json.dump({"customers": decrypted_customers}, out)


def prompt():
    option = input(
        "Enter 1 to create a new key for a restaurant, 2 to decode customer data and 3 to exit script\n"
    )
    if option == "1":
        name = input("Enter the name of your restaurant\n")
        generate_key_values(name)
        print("Public key found in public_key.txt\n")
        prompt()
    elif option == "2":
        print("Please put a dumps.pickle inside the dumps folder\n")
        start = ""
        while start != "y" or start != "n":
            start = input("Enter y to start, n to stop\n")
        if start == "y":
            decrypt()
            print("Your data is in the out directory as out.json")
        else:
            prompt()
    elif option == "3":
        print('Exit by user')
        exit()
    else:
        prompt()


if __name__ == "__main__":
    prompt()
