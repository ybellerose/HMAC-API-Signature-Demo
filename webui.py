from flask import Flask, render_template, request, redirect, url_for, session
import json
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
API_URL = 'http://127.0.0.1:8000/data'

# Load private key
with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

def sign_payload(payload_bytes):
    signature = private_key.sign(
        payload_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        payload = request.form.get('payload', '{}')
        try:
            # Validate JSON
            payload_dict = json.loads(payload)
            payload_str = json.dumps(payload_dict)
        except Exception:
            payload_str = '{}'
            payload_dict = {}
        payload_bytes = payload_str.encode()
        signature = sign_payload(payload_bytes)
        # Store in session for MITM
        session['payload'] = payload_str
        session['signature'] = signature
        return redirect(url_for('mitm'))
    return render_template('index.html', section='post', payload='{"foo": "bar", "number": 123}', signature='', response='')

@app.route('/mitm', methods=['GET', 'POST'])
def mitm():
    payload = session.get('payload', '{}')
    signature = session.get('signature', '')
    if request.method == 'POST':
        # User may have modified payload
        new_payload = request.form.get('payload', payload)
        new_signature = request.form.get('signature', signature)
        session['payload'] = new_payload
        session['signature'] = new_signature
        return redirect(url_for('forward'))
    return render_template('index.html', section='mitm', payload=payload, signature=signature, response='')

@app.route('/forward', methods=['GET', 'POST'])
def forward():
    payload = session.get('payload', '{}')
    signature = session.get('signature', '')
    headers = {
        'Content-Type': 'application/json',
        'x-signature': signature
    }
    try:
        response = requests.post(API_URL, data=payload.encode(), headers=headers)
        result = f"Status: {response.status_code}\n{response.text}"
    except Exception as e:
        result = f"Error: {e}"
    return render_template('index.html', section='response', payload=payload, signature=signature, response=result)

if __name__ == '__main__':
    app.run(debug=True) 