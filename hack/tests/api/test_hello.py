"""API hello tests."""

import pytest

from configmodel.api.app import app


@pytest.fixture
def client():
    """Test fixture."""
    with app.test_client() as testclient:
        yield testclient


def test_0_pass_get(client):  # pylint: disable=W0621
    """Good get."""
    response = client.get("/hello/")
    assert response.status_code == 200
    assert response.json == {"message": "hello!"}


def test_1_pass_get_param(client):  # pylint: disable=W0621
    """Good get with a parameter."""
    response = client.get("/hello/", query_string={"name": "foo"})
    assert response.status_code == 200
    assert response.json == {"message": "hello foo!"}


def test_2_fail_get(client):  # pylint: disable=W0621
    """Bad get."""
    response = client.get("/barf/")
    assert response.status_code == 404
