import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture()
def client():
    snapshot = copy.deepcopy(app_module.activities)
    yield TestClient(app_module.app)
    app_module.activities.clear()
    app_module.activities.update(snapshot)


def test_get_activities_returns_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant(client):
    email = "tester@mergington.edu"
    activity = "Art Studio"

    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in app_module.activities[activity]["participants"]


def test_unregister_removes_participant(client):
    activity = "Chess Club"
    email = app_module.activities[activity]["participants"][0]

    response = client.delete(
        f"/activities/{activity}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
