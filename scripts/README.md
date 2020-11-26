# scripts
Security scripts for tracing.pickeasy.ca

## Usage

Activate Venv
```
source venv venv/bin/activate
```
Navigate to scripts
```
cd scripts
```
Run python script
```
python tracing_scripts.py
>>> Enter 1 to create a new key for a restaurant, 2 to decode customer data and 3 to exit script
>>> 1
>>> Enter your location name
>>> sweet-turtle
>>> Your key
>>> 03dbfcb8d0ad8c951e8f9c63b969ae4bf19b5fec92afed6eb0c7dd6b9d8e301ac6cca2683e44192b7d79e47663964611
>>> Enter 1 to create a new key for a restaurant, 2 to decode customer data and 3 to exit script
>>> 2
>>> Enter target location name
>>> ho-garden
>>> Your data is in out/out.json
>>> Enter 1 to create a new key for a restaurant, 2 to decode customer data and 3 to exit script
>>> 3
>>> exit by user
```

View dumps

```
$ cd out
$ ls
$ out.json .gitignore
```

out.json contains decrypted json data

```
# EXAMPLE
{"customers": [{"name": "Alac wong", "phone_number": "+16475040680", "location": "popeyes", "time_in": "2020-10-16 16:49:29.933000+00:00"}, {"name": "George Qiao", "phone_number": "+16475040680", "location": "popeyes", "time_in": "2020-10-16 16:49:40.149000+00:00"}, {"name": "Raymond Chen", "phone_number": "+16475040680", "location": "popeyes", "time_in": "2020-10-16 16:49:48.792000+00:00"}]}
```

Follow prompt to generate new private/public keys or decrypt customer data.

###Advanced

1. Create new key, this function takes in a slug generates a public/private key value pair. It then uses the public key
and slug to create a new location with a tracing key. The tracing key is then printed out.

2. Decrypt customer data, this function also takes in a slug and which it searches the database for all customers
under location {slug}. Then using the private key in keys.json, it decrypts the customer data and dumps
it into out.json