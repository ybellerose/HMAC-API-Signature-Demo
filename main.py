from fastapi import FastAPI, Request, HTTPException, Header, Depends
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

app = FastAPI()

# Load public key once at startup
with open("public_key.pem", "rb") as key_file:
    PUBLIC_KEY = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

async def verify_signature(request: Request, x_signature: str = Header(...)):
    if request.method == "POST":
        body = await request.body()
        data_to_verify = body
    elif request.method == "GET":
        # Use the raw query string for GET requests
        data_to_verify = request.url.query.encode()
    else:
        data_to_verify = b""
    try:
        signature = base64.b64decode(x_signature)
        PUBLIC_KEY.verify(
            signature,
            data_to_verify,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid signature")

@app.post("/data", dependencies=[Depends(verify_signature)])
async def receive_data(payload: dict):
    return {"message": "Data received and signature verified!", "payload": payload}

@app.get("/data", dependencies=[Depends(verify_signature)])
async def get_data(request: Request):
    # Return the query parameters as a dict
    return {"message": "GET data received and signature verified!", "query_params": dict(request.query_params)} 