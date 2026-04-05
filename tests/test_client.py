import os
import pytest
from hivekey import Hivekey, AsyncHivekey
from hivekey._errors import HivekeyError


class TestHivekeyClient:
    def test_requires_api_key(self):
        os.environ.pop("HIVEKEY_API_KEY", None)
        with pytest.raises(ValueError, match="API key is required"):
            Hivekey()

    def test_creates_with_api_key(self):
        client = Hivekey(api_key="mgent-test123")
        assert client.identity is not None
        assert client.mail is not None
        assert client.vault is not None
        assert client.logs is not None
        assert client.did is not None
        client.close()

    def test_reads_env_var(self):
        os.environ["HIVEKEY_API_KEY"] = "mgent-fromenv"
        try:
            client = Hivekey()
            assert client.identity is not None
            client.close()
        finally:
            del os.environ["HIVEKEY_API_KEY"]

    def test_context_manager(self):
        with Hivekey(api_key="mgent-test") as client:
            assert client.identity is not None


class TestAsyncHivekeyClient:
    def test_requires_api_key(self):
        os.environ.pop("HIVEKEY_API_KEY", None)
        with pytest.raises(ValueError, match="API key is required"):
            AsyncHivekey()


class TestHivekeyError:
    def test_attributes(self):
        err = HivekeyError(401, "unauthorized", "Invalid API key")
        assert err.status == 401
        assert err.code == "unauthorized"
        assert str(err) == "Invalid API key"

    def test_repr(self):
        err = HivekeyError(404, "not_found", "Not found")
        assert "404" in repr(err)
