import hashlib
import hmac
import json
from base64 import b64encode
from typing import Union


def hmac_sha256(payload: bytes, secret: Union[bytes, bytearray]) -> str:
    hashed = hmac.new(key=secret, msg=payload, digestmod=hashlib.sha256).digest()
    base64_encoded = b64encode(hashed)
    return base64_encoded.decode()


def hmac_sha512(payload, secret):
    secret = bytes(secret.encode("utf-8"))
    if isinstance(payload, str):
        body = bytes(payload.encode("utf-8"))
    else:
        body = bytes(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signature = hmac.new(secret, body, digestmod=hashlib.sha512).hexdigest()
    return signature
