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

Run flask command to dump data in parent directory
```
cd ..
flask tracing dump {restaurant_key}
cd dumps
ls
dumps.pickle
```

```
# EXAMPLE
{"customers": [{"name": "Alac wong", "phone_number": "+16475040680", "location": "popeyes", "time_in": "2020-10-16 16:49:29.933000+00:00"}, {"name": "George Qiao", "phone_number": "+16475040680", "location": "popeyes", "time_in": "2020-10-16 16:49:40.149000+00:00"}, {"name": "Raymond Chen", "phone_number": "+16475040680", "location": "popeyes", "time_in": "2020-10-16 16:49:48.792000+00:00"}]}
```
public_key.txt contains generated public key
```
# EXAMPLE
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwuxeCqs2lA+Pnrg1OqDn
amnVuj8aO/l4y4cje3aXBDzH1dJQY2cugB3LW+MzExk8GzDgf7kp36uUjLs5knwd
uHIvNsv/tnFtiAqDDkolOl73dd5fxeiVKFJ3qVnY/1Q35aluc7BFIXuOiuclBBOG
tlS285ejP4XW+P1sovmEbcsk1eic5FZaZRIVyHtVmTiaAAREbVXiNB6LKMkIwOrh
Nczq7KzGb2Btnik6EES6ikNKfr/fBlsOypRKRNxyARIobYRqJOBlbiUUL2JgIWxn
1N587zy7KR3beJZgww3OyfelkQ9qmlXVdnEukP4NaDSUSRD0boTNhiC4laxpBu6N
nwIDAQAB
-----END PUBLIC KEY-----
```