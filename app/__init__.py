import os
from flask import Flask
from app.models import db
from app.views import profile, shorten

def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)

    if testing:
        app.config.from_pyfile("test_config.py")
    else:
        app.config.from_pyfile("config.py")
    app.register_blueprint(profile)
    app.register_blueprint(shorten)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
