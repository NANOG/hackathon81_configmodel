"""API service tests."""

import pytest

from configmodel.api.app import app
from configmodel.database import Base, engine

good_backbone = {
    "schema": "backbone",
    "config": {
        "rtr0.hacktory": {
            "interface": {
                "name": "Ethernet1",
                "ipv4": {"address": "192.0.2.0", "mask": 31},
                "ipv6": {"address": "2001:db8:c057:e110::0", "mask": 127},
            },
        },
        "rtr1.hacktory": {
            "interface": {
                "name": "Ethernet1",
                "ipv4": {"address": "192.0.2.1", "mask": 31},
                "ipv6": {"address": "2001:db8:c057:e110::1", "mask": 127},
            },
        },
    },
}

good_pni = {
    "schema": "pni",
    "config": {
        "rtr1.hacktory": {
            "interface": {
                "name": "Ethernet2",
                "ipv4": {"address": "172.16.0.0", "mask": 31},
                "ipv6": {"address": "2001:db8:c0ff:ee::0", "mask": 127},
            },
            "bgppeer": {
                "local_asn": 666,
                "peer_asn": 1337,
                "peer_v4": "172.16.0.1",
                "peer_v6": "2001:db8:c0ff:ee::1",
            },
        },
    },
}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_0_0_cleanup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_0_service_pass_get(client):
    # runs zeroeth and gets an emtpy list
    response = client.get("/service/")
    assert response.status_code == 200
    assert response.json == []


def test_1_service_post_pass(client):
    # runs first and creates a service
    post_data = good_backbone
    expected_data = good_backbone
    expected_data["service_id"] = 1
    response = client.post("/service/", json=post_data)
    assert response.status_code == 201
    assert response.json == expected_data


def test_2_service_pass_get(client):
    expected_data = good_backbone
    expected_data["service_id"] = 1
    response = client.get("/service/")
    assert response.status_code == 200
    assert response.json == [expected_data]


def test_3_service_pass_get_1(client):
    expected_data = good_backbone
    expected_data["service_id"] = 1
    response = client.get("/service/1")
    assert response.status_code == 200
    assert response.json == expected_data


def test_4_service_pass_post_another(client):
    post_data = good_pni
    expected_data = good_pni
    expected_data["service_id"] = 2
    response = client.post("/service/", json=post_data)
    assert response.status_code == 201
    assert response.json == expected_data


def test_5_service_pass_delete(client):
    response = client.delete("/service/2")
    assert response.status_code == 204


def test_6_service_fail_delete_no_id(client):
    response = client.delete("/service/666")
    assert response.status_code == 404


def test_7_service_fail_post_no_schema(client):
    post_data = {"config": {"name": "Ethernet2"}}
    response = client.post("/service/", json=post_data)
    assert response.status_code == 400


def test_8_service_pass_render(client):
    params = {"family": "eos"}
    response = client.get(
        "/render/service/1", query_string=params
    )  # service 1 is a backbone
    assert response.status_code == 200
    assert response.json == [
        {
            "hostname": "rtr0.hacktory",
            "config": """interface Ethernet1
    ip address 192.0.2.0/31
    ipv6 address 2001:db8:c057:e110::0/127
    no lldp transmit
    no lldp receive
""",
        },
        {
            "hostname": "rtr1.hacktory",
            "config": """interface Ethernet1
    ip address 192.0.2.1/31
    ipv6 address 2001:db8:c057:e110::1/127
    no lldp transmit
    no lldp receive
""",
        },
    ]
