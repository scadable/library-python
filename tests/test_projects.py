import respx
from httpx import Response

from scadable import Project


def test_list_projects(client, mock_api):
    mock_api.get("/api/projects").mock(
        return_value=Response(
            200,
            json=[
                {
                    "id": "p1",
                    "name": "My Project",
                    "description": "Test",
                    "owner_email": "a@b.com",
                },
                {"id": "p2", "name": "Other", "description": None},
            ],
        )
    )

    projects = client.projects.list()
    assert len(projects) == 2
    assert isinstance(projects[0], Project)
    assert projects[0].id == "p1"
    assert projects[0].name == "My Project"
    assert projects[1].id == "p2"


def test_get_project(client, mock_api):
    mock_api.get("/api/projects/p1").mock(
        return_value=Response(
            200,
            json={
                "id": "p1",
                "name": "My Project",
                "description": "Desc",
                "owner_email": "a@b.com",
            },
        )
    )

    project = client.projects.get(project_id="p1")
    assert isinstance(project, Project)
    assert project.id == "p1"
    assert project.name == "My Project"
