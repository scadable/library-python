import pytest
from scadable import Scadable, AsyncScadable


def test_init_with_api_key():
    client = Scadable(api_key="sk_test")
    assert client._config.api_key == "sk_test"
    assert client._config.base_url == "https://api.scadable.com"
    client.close()


def test_init_from_env(monkeypatch):
    monkeypatch.setenv("SCADABLE_API_KEY", "sk_from_env")
    client = Scadable()
    assert client._config.api_key == "sk_from_env"
    client.close()


def test_init_custom_base_url():
    client = Scadable(api_key="sk_test", base_url="https://custom.example.com")
    assert client._config.base_url == "https://custom.example.com"
    client.close()


def test_init_no_key_raises():
    with pytest.raises(ValueError, match="No API key"):
        Scadable()


def test_context_manager():
    with Scadable(api_key="sk_test") as client:
        assert client._config.api_key == "sk_test"


def test_has_gateways_resource():
    with Scadable(api_key="sk_test") as client:
        assert hasattr(client, "gateways")


@pytest.mark.asyncio
async def test_async_context_manager():
    async with AsyncScadable(api_key="sk_test") as client:
        assert client._config.api_key == "sk_test"
        assert hasattr(client, "gateways")
