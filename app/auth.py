import re
from flask import redirect, url_for, flash
from app.models import User
from app.constants import USER_FIELD_REGEX

def verify_user(func):
    def wrapper(*args, **kwargs):
        if session.get("username") and not User.query.get(session["username"]):
            session["username"] = None
        return func(*args, **kwargs)
    return wrapper

def validate_user_fields(username, password):
    valid_username = bool(re.search(USER_FIELD_REGEX, username))
    valid_password = bool(re.search(USER_FIELD_REGEX, password))
    return valid_username and valid_password
