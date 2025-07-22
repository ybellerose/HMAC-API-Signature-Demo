import requests
import json
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import base64

API_URL = 'http://127.0.0.1:8000/data'

payload = {"foo": "bar", "number": 123}
body = json.dumps(payload).encode()

# Load private key
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# POST example
signature_post = private_key.sign(
    body,
    padding.PKCS1v15(),
    hashes.SHA256()
)
signature_post_b64 = base64.b64encode(signature_post).decode()
headers_post = {
    'Content-Type': 'application/json',
    'x-signature': signature_post_b64
}
response_post = requests.post(API_URL, data=body, headers=headers_post)
print("POST Example:")
print(f"Status code: {response_post.status_code}")
print(f"Response: {response_post.text}\n")

# GET example
params = {"foo": "bar", "number": 123}
from urllib.parse import urlencode
query_string = urlencode(params)
signature_get = private_key.sign(
    query_string.encode(),
    padding.PKCS1v15(),
    hashes.SHA256()
)
signature_get_b64 = base64.b64encode(signature_get).decode()
headers_get = {
    'x-signature': signature_get_b64
}
response_get = requests.get(API_URL, params=params, headers=headers_get)
print("GET Example:")
print(f"Status code: {response_get.status_code}")
print(f"Response: {response_get.text}") 