import pytest
from httpx import Response

from scadable import ScadableError, AuthenticationError, NotFoundError


def test_401_raises_auth_error(client, mock_api):
    mock_api.get("/api/me").mock(
        return_value=Response(401, json={"error": "invalid token"})
    )

    with pytest.raises(AuthenticationError, match="invalid token"):
        client.users.me()


def test_404_raises_not_found(client, mock_api):
    mock_api.get("/api/projects/bad-id").mock(
        return_value=Response(404, json={"error": "project not found"})
    )

    with pytest.raises(NotFoundError, match="project not found"):
        client.projects.get(project_id="bad-id")


def test_500_raises_server_error(client, mock_api):
    from scadable import InternalServerError

    mock_api.get("/api/projects").mock(
        return_value=Response(500, json={"error": "internal error"})
    )

    with pytest.raises(InternalServerError):
        client.projects.list()


def test_error_has_status_and_body(client, mock_api):
    mock_api.get("/api/me").mock(return_value=Response(401, json={"error": "bad key"}))

    with pytest.raises(AuthenticationError) as exc_info:
        client.users.me()

    err = exc_info.value
    assert err.status_code == 401
    assert err.body == {"error": "bad key"}
    assert err.message == "bad key"
