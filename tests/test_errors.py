import pytest
from httpx import Response

from scadable import AuthenticationError, NotFoundError


def test_401_raises_auth_error(client, mock_api):
    mock_api.get("/v1/gateways").mock(
        return_value=Response(401, json={"error": "invalid token"})
    )
    with pytest.raises(AuthenticationError, match="invalid token"):
        client.gateways.list()


def test_404_raises_not_found(client, mock_api):
    mock_api.get("/v1/gateways/bad-id").mock(
        return_value=Response(404, json={"error": "gateway not found"})
    )
    with pytest.raises(NotFoundError, match="gateway not found"):
        client.gateways.get("bad-id")


def test_500_raises_server_error(client, mock_api):
    from scadable import InternalServerError

    mock_api.get("/v1/gateways").mock(
        return_value=Response(500, json={"error": "internal error"})
    )
    with pytest.raises(InternalServerError):
        client.gateways.list()


def test_error_has_status_and_body(client, mock_api):
    mock_api.get("/v1/gateways").mock(
        return_value=Response(401, json={"error": "bad key"})
    )
    with pytest.raises(AuthenticationError) as exc_info:
        client.gateways.list()

    err = exc_info.value
    assert err.status_code == 401
    assert err.body == {"error": "bad key"}
    assert err.message == "bad key"
