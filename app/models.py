from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text, nullable=False)

class Link(db.Model):
    long_link = db.Column(db.Text, primary_key=True)
    short_link = db.Column(db.String(10), unique=True)

class UserLink(db.Model):
    username = db.Column(db.Text, db.ForeignKey(User.username), primary_key=True)
    long_link = db.Column(db.Text, db.ForeignKey(Link.long_link), primary_key=True)
