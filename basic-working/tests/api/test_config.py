"""API config tests."""

import pytest

from configmodel.api.app import app
from configmodel.database import Base, engine


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_0_0_cleanup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_0_config_pass_get(client):
    # runs zeroeth and gets an emtpy list
    response = client.get("/config/")
    assert response.status_code == 200
    assert response.json == []


def test_1_config_pass_post(client):
    # runs first and creates a config
    post_data = {
        "hostname": "rtr0.hacktory",
        "schema": "interface",
        "config": {"name": "Ethernet1"},
    }
    response = client.post("/config/", json=post_data)
    assert response.status_code == 201
    assert response.json == {
        "config_id": 1,
        "hostname": "rtr0.hacktory",
        "schema": "interface",
        "config": {"name": "Ethernet1"},
    }


def test_2_config_pass_get(client):
    response = client.get("/config/")
    assert response.status_code == 200
    assert response.json == [
        {
            "config_id": 1,
            "hostname": "rtr0.hacktory",
            "schema": "interface",
            "config": {"name": "Ethernet1"},
        }
    ]


def test_3_config_pass_get_1(client):
    response = client.get("/config/1")
    assert response.status_code == 200
    assert response.json == {
        "config_id": 1,
        "hostname": "rtr0.hacktory",
        "schema": "interface",
        "config": {"name": "Ethernet1"},
    }


def test_4_config_pass_post_another(client):
    post_data = {
        "hostname": "rtr0.hacktory",
        "schema": "interface",
        "config": {"name": "Ethernet2"},
    }
    response = client.post("/config/", json=post_data)
    assert response.status_code == 201
    assert response.json == {
        "config_id": 2,
        "hostname": "rtr0.hacktory",
        "schema": "interface",
        "config": {"name": "Ethernet2"},
    }


def test_5_config_pass_delete(client):
    response = client.delete("/config/2")
    assert response.status_code == 204


def test_6_config_fail_post_no_hostname(client):
    post_data = {"schema": "interface", "config": {"name": "Ethernet2"}}
    response = client.post("/config/", json=post_data)
    assert response.status_code == 400


def test_7_config_fail_post_invalid_config(client):
    post_data = {
        "schema": "interface",
        "hostname": "rtr0.hacktory",
        "config": {"foo": "bar"},
    }
    response = client.post("/config/", json=post_data)
    assert response.status_code == 400


def test_8_config_fail_get_no_config(client):
    response = client.get("/config/666")
    assert response.status_code == 404


def test_9_config_pass_render(client):
    params = {"family": "eos"}
    response = client.get("/render/config/1", query_string=params)
    assert response.status_code == 200
    assert response.json == {
        "hostname": "rtr0.hacktory",
        "config": """interface Ethernet1
    no lldp transmit
    no lldp receive
""",
    }
