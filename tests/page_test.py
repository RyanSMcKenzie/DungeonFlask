import unittest
import app

def test_test():
    assert app.mainPage()['username'] == "admin"