# Asymmetric Signature API Example

This project demonstrates a simple FastAPI server that verifies digital signatures (RSA) on every POST request, and a Python client that signs requests using a private key.

## Features
- **Asymmetric cryptography (RSA)** for signing and verifying requests
- **FastAPI** backend
- **Python client** for sending signed requests

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate RSA key pair
This will create `private_key.pem` and `public_key.pem` in the project directory.
```bash
python generate_keys.py
```

---

## Running the Server
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
- The API will be available at `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

---

## Using the Client
The client script will:
- Sign a JSON payload with the private key
- Send the payload and signature to the server

Run the client:
```bash
python client.py
```

You should see a response like:
```
Status code: 200
Response: {"message": "Data received and signature verified!", "payload": {"foo": "bar", "number": 123}}
```

---

## How it Works
- The **client** signs the request body using its RSA private key and sends the signature in the `x-signature` header (base64 encoded).
- The **server** verifies the signature using the public key before processing the request.

---

## Files
- `main.py` - FastAPI server with signature verification
- `client.py` - Example client that signs and sends a request
- `generate_keys.py` - Script to generate RSA key pair
- `requirements.txt` - Python dependencies

---

## Notes
- This example uses a single key pair for simplicity. For multiple clients, you would manage multiple public keys on the server.
- Never share your private key. Keep it secure! 