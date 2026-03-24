import pytest
import respx
from httpx import Response

from scadable import Scadable, AsyncScadable


@pytest.fixture
def mock_api():
    with respx.mock(base_url="https://test.scadable.com") as mock:
        yield mock


@pytest.fixture
def client(mock_api):
    return Scadable(api_key="sk_test_123", base_url="https://test.scadable.com")


@pytest.fixture
def async_client(mock_api):
    return AsyncScadable(api_key="sk_test_123", base_url="https://test.scadable.com")
