import json
import re
import unittest
from flask import session
from werkzeug.security import generate_password_hash
from app import create_app
from app.models import db, User, Link, UserLink

class APITest(unittest.TestCase):
    def setUp(self):
        app = create_app(testing=True)
        self.app = app
        self.test_client = app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def login_user(self, username):
        with self.app.app_context():
            user = User(username=username, password=generate_password_hash("test"))
            db.session.add(user)
            db.session.commit()

        self.test_client.post("/login", data={"username": "test", "password": "test"})

class ProfileViewTest(APITest):
    def test_register(self):
        with self.test_client:
            response = self.test_client.post("/register", data={"username": "test", "password": "test"})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "/")
            user = User.query.get("test")
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "test")
            self.assertEqual(session.get("username"), "test")

    def test_logout(self):
        with self.test_client:
            self.test_client.post("/register", data={"username": "test", "password": "test"})
            response = self.test_client.post("/logout")
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "/")
            self.assertIsNone(session.get("username"))

    def test_login(self):
        with self.app.app_context():
            user = User(username="test", password=generate_password_hash("test"))
            db.session.add(user)
            db.session.commit()

        with self.test_client:
            response = self.test_client.post("/login", data={"username": "test", "password": "test"})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, "/")
            self.assertEqual(session.get("username"), "test")

class ShortenViewTest(APITest):
    def test_shorten_link(self):
        response = self.test_client.post("/", data={"link": "http://test.com"})
        short_link = json.loads(response.get_data(as_text=True))["short_link"]
        match = re.search("^[a-zA-Z0-9]{8}$", short_link)
        self.assertIsNotNone(match)

        with self.app.app_context():
            link = Link.query.get("http://test.com")
            self.assertIsNotNone(link)

    def test_shorten_link_logged_in(self):
        self.login_user("test")

        self.test_client.post("/", data={"link": "http://test.com"})

        with self.app.app_context():
            userlink = UserLink.query.get(("test", "http://test.com"))
            self.assertIsNotNone(userlink)

    def test_reroute(self):
        shorten_response = self.test_client.post("/", data={"link": "http://test.com"})
        short_link = json.loads(shorten_response.get_data(as_text=True))["short_link"]

        reroute_response = self.test_client.get(f"/{short_link}")
        self.assertEqual(reroute_response.status_code, 302)
        self.assertEqual(reroute_response.location, "http://test.com")
