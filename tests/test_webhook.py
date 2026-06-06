"""Tests for mailgent.webhook.verify_webhook.

Mirrors the four-test shape of the Node SDK's webhook tests so both
SDKs behave identically against the same API output.
"""

import hashlib
import hmac

from mailgent.webhook import verify_webhook

SECRET = "whsec_test_supersecret"


def _hex(secret: str, body: str) -> str:
    return hmac.new(
        secret.encode("utf-8"), body.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def test_returns_true_on_valid_sha256_signature():
    body = '{"event":"payment.received","id":"pay_42"}'
    sig = _hex(SECRET, body)
    assert verify_webhook(body, f"sha256={sig}", SECRET) is True


def test_returns_false_when_signature_does_not_match():
    body = '{"event":"payment.received"}'
    wrong = _hex("different-secret", body)
    assert verify_webhook(body, f"sha256={wrong}", SECRET) is False


def test_returns_false_when_signature_header_missing():
    assert verify_webhook("{}", None, SECRET) is False
    assert verify_webhook("{}", "", SECRET) is False


def test_returns_false_when_sha256_prefix_missing():
    body = "{}"
    sig = _hex(SECRET, body)
    assert verify_webhook(body, sig, SECRET) is False


def test_returns_false_when_secret_is_empty():
    body = '{"event":"payment.received"}'
    any_sig = "sha256=" + "ab" * 32
    assert verify_webhook(body, any_sig, "") is False


def test_accepts_bytes_body():
    body_str = '{"event":"payment.received"}'
    body_bytes = body_str.encode("utf-8")
    sig = _hex(SECRET, body_str)
    assert verify_webhook(body_bytes, f"sha256={sig}", SECRET) is True


def test_returns_false_when_signature_contains_non_hex():
    assert verify_webhook("{}", "sha256=not-hex!!!", SECRET) is False
