import uuid
import random
import math
import hashlib
from functools import wraps
from flask import request, session, current_app

from authlib.jose import jwt
from datetime import datetime

def create_access_token(key, alg, payload):
    key = open(key, 'rb').read()
    # Encode payload by alg and decode the bytes result to produce a string.
    return jwt.encode({'alg': alg}, payload, key).decode("utf-8")

def create_refresh_token():
    plain = uuid.uuid4().hex
    refresh_token = hashlib.shake_256(plain.encode('utf-8')).hexdigest(50)
    return refresh_token

def create_verify_link(key, plain):
    pass

def get_verify_code(digit):
    return str(random.randint(0, int(math.pow(10, 5)) - 1)).zfill(5)