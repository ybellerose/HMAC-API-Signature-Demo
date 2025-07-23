# Asymmetric Signature API Example

## Disclaimer WARNING

This code is strictly for recreational purposes only! If you're even thinking about putting this into production, please consult a highly qualified veterinarian. We're not saying kitten deaths will occur, but if your server starts purring ominously and coughing up hairballs, don't say we didn't warn you.

And remember, when disaster strikes, there's always a conveniently small, furry scapegoat.

## Project 

This project demonstrates a simple FastAPI server that verifies digital signatures (RSA) on every POST request, a Python client that signs requests using a private key, and a Flask/Tailwind web UI that lets you interactively explore man-in-the-middle (MITM) interception and modification of signed requests.

## Features
- **Asymmetric cryptography (RSA)** for signing and verifying requests
- **FastAPI** backend
- **Python client** for sending signed requests
- **Flask + Tailwind web UI** for interactive MITM demonstration

---

## Setup

### 1. Install dependencies
All required dependencies are pinned in `requirements.txt`:
```
cryptography==42.0.5
fastapi==0.115.12
flask==2.3.3
requests==2.31.0
uvicorn==0.34.2
```
Install them with:
```bash
pip install -r requirements.txt
```

### 2. Generate RSA key pair
This will create `private_key.pem` and `public_key.pem` in the project directory.
```bash
python generate_keys.py
```

---

## Running the FastAPI Server
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
- The API will be available at `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

---

## Using the Client Script
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

## Web UI: Man-in-the-Middle (MITM) Demo

The web UI lets you interactively explore how digital signatures protect data in transit, and what happens if a payload or signature is intercepted and modified.

### Running the Web UI
```bash
python webui.py
```
Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### How the Web UI Works
The UI is divided into three steps:

1. **POST Payload**
    - Enter a JSON payload (default: `{ "foo": "bar", "number": 123 }`).
    - The payload is signed with your private key and sent to the next step.
    - _Explanation shown in the UI._

2. **Man in the Middle (MITM)**
    - Here you can **intercept and modify** the payload or the signature before forwarding to the endpoint.
    - This simulates a man-in-the-middle attack or a proxy.
    - Try changing the payload or signature to see how the endpoint reacts!
    - _Clear instructions are shown in the UI._

3. **Endpoint Response**
    - Shows the payload and signature sent to the endpoint, and the endpoint's response.
    - If the payload or signature was modified, the endpoint will likely reject the request.
    - _Explanation is shown in the UI._

---

## How it Works
- The **client** and web UI sign the request body using the RSA private key and send the signature in the `x-signature` header (base64 encoded).
- The **server** verifies the signature using the public key before processing the request.
- If the payload or signature is changed in transit, the server will detect it and reject the request.

---

## Files
- `main.py` - FastAPI server with signature verification
- `client.py` - Example client that signs and sends a request
- `webui.py` - Flask web UI for MITM demonstration
- `templates/index.html` - Tailwind-styled HTML template for the web UI
- `generate_keys.py` - Script to generate RSA key pair
- `requirements.txt` - Python dependencies (pinned versions)

---

## Notes
- This example uses a single key pair for simplicity. For multiple clients, you would manage multiple public keys on the server.
- Never share your private key. Keep it secure!
- The web UI is for demonstration and educational purposes. 