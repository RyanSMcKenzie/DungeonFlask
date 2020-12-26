import unittest
from app import app, mainPage, user_ref, sheet_ref
import pytest
import os
# Run me with python3 -m pytest -v

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

def sessionData(client):
    return client.get('/test-session')

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_test(client):
    # Tests logging a user in
    with app.test_request_context('/login', 
    data={"username":app.config["username"], 
    "password":app.config["password"]}):
        login(client, app.config["username"], app.config["password"])
        print(sessionData(client))
        assert sessionData(client).data.decode('utf-8') == 'admin'
        logout(client)
        assert sessionData(client).data.decode('utf-8') == 'No user'

def register(client, username, password, password2):
    return client.post('/register', data=dict(
        username=username,
        password=password,
        password2=password2
    ), follow_redirects=True)

def makeNewSheet(client):
    return client.post('/new-character')

def log_req(client):
    return client.get('/test-login-requirement')

def saveChar(client):
    data = sheet_ref.document(u'9JxW3AAKWMaUoSrWAHeI').get().to_dict()
    data["sheetID"] = "testing_it_up"
    return client.post('/save-character', data=data)

def test_register(client):
    # Tests registering a new account - add and delete account
    with app.test_request_context('/register', 
    data={"username":"Bilbo", 
    "password":"Billpass",
    "password2":"Billpass"}):
        register(client, "Bilbo", "Billpass", "Billpass")
        assert user_ref.where('username', 
        '==', "Bilbo").get() != []
        assert user_ref.where('username', 
        '==', "Bilbo").get()[0].get('username') == "Bilbo"
        del_id = user_ref.where('username', '==', 'Bilbo').get()[0].id
        user_ref.document(del_id).delete()
        assert user_ref.where('username', '==', "Bilbo").get() == []

def test_sheet(client):
    with app.test_request_context('/new-character'):
        userID = user_ref.where('username', '==', app.config['username']).get()[0].id
        sheets = sheet_ref.where('userID', '==', userID).get()
        makeNewSheet(client)
        new_sheets = sheet_ref.where('userID', '==', userID).get()
        assert len(new_sheets) - len(sheets) == 0

    with app.test_request_context('/login', 
    data={"username":app.config["username"], 
    "password":app.config["password"]}):
        login(client, app.config["username"], app.config["password"])

    with app.test_request_context('/save-character'):
        saveChar(client)
        new_sheets = sheet_ref.where('userID', '==', userID).get()
        assert len(new_sheets) - len(sheets) == 1
        sheet_ref.document(u"testing_it_up").delete()
        new_sheets = sheet_ref.where('userID', '==', userID).get()
        assert len(new_sheets) - len(sheets) == 0
        logout(client)
        assert sessionData(client).data.decode('utf-8') == 'No user'

def test_login_req(client):
    with app.test_request_context('/test-login-requirement'):
        assert log_req(client).data.decode('utf-8') != "Logged in"
        login(client, app.config["username"], app.config["password"])
        assert log_req(client).data.decode('utf-8') == "Logged in"
        logout(client)
        assert log_req(client).data.decode('utf-8') != "Logged in"