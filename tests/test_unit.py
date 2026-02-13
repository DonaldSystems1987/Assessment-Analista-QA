import pytest
from fastapi import HTTPException
from app.main import create_token, verify_token, require_admin
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret123"
ALGORITHM = "HS256"



class DummyCredentials:
    def __init__(self, token):
        self.credentials = token


def test_create_token_contains_username_and_role():
    token = create_token("admin", "admin")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "admin"
    assert payload["role"] == "admin"
    assert "exp" in payload


def test_verify_token_valid():
    token = create_token("admin", "admin")
    creds = DummyCredentials(token)
    payload = verify_token(creds)
    assert payload["sub"] == "admin"
    assert payload["role"] == "admin"

def test_verify_token_invalid():
    creds = DummyCredentials("badtoken")
    with pytest.raises(HTTPException) as exc:
        verify_token(creds)
    assert exc.value.status_code == 401

def test_require_admin_success():
    token = create_token("admin", "admin")
    creds = DummyCredentials(token)
    payload = verify_token(creds)
    result = require_admin(payload)
    assert result["role"] == "admin"

def test_require_admin_fail():
    token = create_token("user", "user")
    creds = DummyCredentials(token)
    payload = verify_token(creds)
    with pytest.raises(HTTPException) as exc:
        require_admin(payload)
    assert exc.value.status_code == 403

def test_expired_token():
 
    exp_time = datetime.utcnow() - timedelta(seconds=1)
    payload = {"sub": "admin", "role": "admin", "exp": int(exp_time.timestamp())}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    creds = DummyCredentials(token)

    
    result = verify_token(creds)
    assert result["sub"] == "admin"
    assert result["role"] == "admin"
