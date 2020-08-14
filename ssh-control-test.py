import gnupg
import requests
import json
import time 
import sys
import uuid 
import secrets

import logging 

# Change this if needed
HOST = 'http://127.1:5000/' # Default Flask Debug Server Address

# Test Index

response = requests.get(HOST)
if response.status_code != 200:
    print("Bad Response: {}".format(response.status_code))
    sys.exit(-1)


json_parsed = json.loads(response.content)
print(json_parsed)

# Try sending invalid operations
print("Sending 10 invalid operations")

for i in range(10):
    print("Request #1")
    operation = uuid.uuid4()
    response = requests.post(HOST + 'request', {"operation": operation})
    print(response.content)
    print()

# Try to spoof ssh on operation
operation = 'request-ssh-on'
print("Sending Operation: {}".format(operation))
response = requests.post(HOST + 'request', {"operation": operation})
print(response.content)

json_parsed = json.loads(response.content)
print(json_parsed)


head = {"Authorization" : "Bearer {}".format(json_parsed['request_token'])}
secret = secrets.token_hex(1024) # Lets try a secret of same length 

execute_response = requests.post(HOST + 'execute', data={"secret": "{}".format(secret) }, headers=head)
print(execute_response)

json_parsed_execute = json.loads(execute_response.content)
print(json_parsed_execute)


# Lets Try If we can verify past the expiry date of the JWT.
# Lets assume the possibility that the PGP message can be decrypted without the Private Key with the help of a 
# Quantum Computer but it is only possible if we can try after 60 seconds.
# Please Note that if it is possible to crack the encrypted message under 60 seconds then this software is 
# useless.

operation = 'request-ssh-on'
print("Sending Operation: {}".format(operation))
response = requests.post(HOST + 'request', {"operation": operation})
print(response.content)

json_parsed = json.loads(response.content)
print(json_parsed)


head = {"Authorization" : "Bearer {}".format(json_parsed['request_token'])}

print("Quantum Computer is Cracking GPG Private Key and Decrypting Secret")
time.sleep(60)
secret = secrets.token_hex(1024) # Lets assume this is the cracked secret

execute_response = requests.post(HOST + 'execute', data={"secret": "{}".format(secret) }, headers=head)
print(execute_response)

json_parsed_execute = json.loads(execute_response.content)
print(json_parsed_execute)


# Lets try brute forcing the secret


operation = 'request-ssh-on'
print("Sending Operation: {}".format(operation))
response = requests.post(HOST + 'request', {"operation": operation})
print(response.content)

json_parsed = json.loads(response.content)
print(json_parsed)


head = {"Authorization" : "Bearer {}".format(json_parsed['request_token'])}

print("Brute forcing 10 secrets")
for i in range(10):
    secret = secrets.token_hex(1024) # Lets assume this is the cracked secret
    execute_response = requests.post(HOST + 'execute', data={"secret": "{}".format(secret) }, headers=head)
    print(execute_response)
    json_parsed_execute = json.loads(execute_response.content)
    print(json_parsed_execute)

