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

```

Follow prompt to generate new private/public keys or decrypt customer data.

## Miscellaneous

out and dumps directory can be found inside script when indicated by prompt

```
cd dumps
# put your pickle.dumps here when indicated by prompt
cd ..
cd out
ls
out.json public_key.txt
```

How to get dumps.pickle?

Tracing api provides data dumps for encrypted customer data which is decrypted by the following scripts
Go to
```
https://tracing.pickeasy.ca/locations/{restaurant_name}/customers
```
and a dumps.pickle of the customer data will be downloaded for you.

out.json contains decrypted customer data of your dumps.pickle
public_key.txt contains the generated public key when the user creates the key