import unittest
from app import app, mainPage
import pytest
import os

@pytest.fixture
def client():
    app.secret_key = os.urandom(12)
    app.config["username"] = "admin"
    app.config["password"] = "adminpass"

    return app.test_client()

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_test(client):
    with app.test_request_context('/login', 
    data={"username":app.config["username"], 
    "password":app.config["password"]}):
        assert login(client, app.config["username"], 
        app.config["password"]).data.decode('utf-8') == "Hi admin"
        logout(client)