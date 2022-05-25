import json
import pytest

from app.api.models import Fleet
#from app.api.schemas import Fleet

def test_create_fleet(test_app, monkeypatch):
    test_payload = {"id": "6", "name": "abc"}

    async def mock_post(name, id):
        return 1

    monkeypatch.setattr(Fleet, "create", mock_post)

    response = test_app.post("/fleet/", data=json.dumps(test_payload),)

    assert response.status_code == 201
    assert response.json() == test_payload


def test_create_note_invalid_json(test_app):
    response = test_app.post("/fleet/", data=json.dumps({"name": "something"}))
    assert response.status_code == 422

def test_read_fleet(test_app, monkeypatch):
    test_data = {"name":"AA","id":1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(Fleet, "get", mock_get)

    response = test_app.get("/fleet/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_fleet_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(Fleet, "get", mock_get)

    response = test_app.get("/fleet/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Fleet not found"

def test_read_all_notes(test_app, monkeypatch):
    test_data = [
        {"name":"AA","id":1},{"name":"BB","id":2},
        {"name":"CC","id":3},{"name":"DD","id":4}
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(Fleet, "get_all", mock_get_all)

    response = test_app.get("/fleets/")
    assert response.status_code == 200
    assert response.json() == test_data

def test_remove_note(test_app, monkeypatch):
    test_data = {"id": "1", "name": "AA"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(Fleet, "get", mock_get)

    async def mock_delete(id):
        return {"detail": "Delete succesfully"}

    monkeypatch.setattr(Fleet, "delete", mock_delete)

    response = test_app.delete("/fleet/1/")
    assert response.status_code == 200
    assert response.json() == {"detail": "Delete succesfully"}


def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(Fleet, "get", mock_get)

    response = test_app.delete("/fleet/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

