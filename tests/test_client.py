import os
import pytest
from mailgent import Mailgent, AsyncMailgent
from mailgent._errors import MailgentError


class TestMailgentClient:
    def test_requires_api_key(self):
        os.environ.pop("MAILGENT_API_KEY", None)
        with pytest.raises(ValueError, match="API key is required"):
            Mailgent()

    def test_creates_with_api_key(self):
        client = Mailgent(api_key="mgent-test123")
        assert client.identity is not None
        assert client.mail is not None
        assert client.vault is not None
        assert client.logs is not None
        assert client.did is not None
        client.close()

    def test_reads_env_var(self):
        os.environ["MAILGENT_API_KEY"] = "mgent-fromenv"
        try:
            client = Mailgent()
            assert client.identity is not None
            client.close()
        finally:
            del os.environ["MAILGENT_API_KEY"]

    def test_context_manager(self):
        with Mailgent(api_key="mgent-test") as client:
            assert client.identity is not None


class TestAsyncMailgentClient:
    def test_requires_api_key(self):
        os.environ.pop("MAILGENT_API_KEY", None)
        with pytest.raises(ValueError, match="API key is required"):
            AsyncMailgent()


class TestMailgentError:
    def test_attributes(self):
        err = MailgentError(401, "unauthorized", "Invalid API key")
        assert err.status == 401
        assert err.code == "unauthorized"
        assert str(err) == "Invalid API key"

    def test_repr(self):
        err = MailgentError(404, "not_found", "Not found")
        assert "404" in repr(err)
