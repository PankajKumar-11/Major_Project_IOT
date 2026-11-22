"""
Unit Tests for Authentication and Challenge-Response Module.
"""
import pytest
from database.db_manager import DatabaseManager
from core.authentication import AuthenticationManager

def test_device_registration_and_auth(tmp_path):
    db_file = tmp_path / "test_auth.db"
    db = DatabaseManager(db_file)
    auth = AuthenticationManager(db)

    # 1. Register device
    dev_id = "test_sensor_99"
    secret = "secure_key_123"
    auth.register_device(dev_id, "sensor", "monitor", secret)

    # 2. Verify in DB
    dev = db.get_device(dev_id)
    assert dev is not None
    assert dev["auth_status"] == "UNAUTHENTICATED"

    # 3. Authenticate with wrong password
    ok, msg = auth.authenticate_device(dev_id, "wrong_password")
    assert not ok
    assert auth.get_failure_count(dev_id) == 1

    # 4. Authenticate with correct password
    ok, msg = auth.authenticate_device(dev_id, secret)
    assert ok
    assert auth.get_failure_count(dev_id) == 0
    dev_updated = db.get_device(dev_id)
    assert dev_updated["auth_status"] == "AUTHENTICATED"

def test_nonce_challenge_response(tmp_path):
    db_file = tmp_path / "test_challenge.db"
    db = DatabaseManager(db_file)
    auth = AuthenticationManager(db)

    dev_id = "test_sensor_99"
    secret = "secure_key_123"
    auth.register_device(dev_id, "sensor", "monitor", secret)

    # Issue challenge nonce
    nonce = auth.issue_challenge(dev_id, ttl_seconds=10.0)
    assert len(nonce) == 32

    # Invalidate with bogus token
    assert not auth.verify_challenge_response(dev_id, nonce, "invalid_token", secret)

    # Issue another nonce and verify with legitimate HMAC
    nonce2 = auth.issue_challenge(dev_id, ttl_seconds=10.0)
    import hmac, hashlib
    valid_token = hmac.new(secret.encode(), nonce2.encode(), hashlib.sha256).hexdigest()
    assert auth.verify_challenge_response(dev_id, nonce2, valid_token, secret)

