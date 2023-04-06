from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy import exc, text
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import verify_user, validate_user_fields
from app.models import db, User

profile = Blueprint("profile", __name__)

@verify_user
@profile.route('/login', methods=["GET", "POST"])
def login():
    if session.get("username"):
        return redirect(url_for("shorten.shortener"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not validate_user_fields(username, password):
            flash("Invalid username or password.")
            return redirect(url_for("profile.login"))

        user = None
        if username and password:
            user = User.query.get(username)

        if user and check_password_hash(user.password, password):
            session["username"] = user.username
            return redirect(url_for("shorten.shortener"))
        else:
            flash("Incorrect username or password.")
            return redirect(url_for("profile.login"))

    return render_template("login.html", username=session.get("username"))

@profile.route('/logout', methods=["POST"])
def logout():
    session["username"] = None
    return redirect(url_for("shorten.shortener"))

@verify_user
@profile.route('/register', methods=["GET", "POST"])
def register():
    if session.get("username"):
        return redirect(url_for("shorten.shortener"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not validate_user_fields(username, password):
            return redirect(url_for("profile.register"))

        hashed_pw = generate_password_hash(password)

        try:
            user = User(username=username, password=hashed_pw)
            db.session.add(user)
            db.session.commit()

            session["username"] = user.username

            return redirect(url_for("shorten.shortener"))
        except exc.IntegrityError:
            db.session.rollback()
            flash("Username already in use.")
            return redirect(url_for("profile.register"))

    return render_template("register.html", username=session.get("username"))

@verify_user
@profile.route("/links", methods=["GET"])
def links():
    if not session.get("username"):
        flash("Please login to view saved links.")
        return redirect(url_for("profile.login"))

    query = text("""
        select l.long_link, l.short_link
        from
            user_link ul
            join link l
            on ul.long_link = l.long_link
        where username = :username
    """)

    links = db.session.execute(query, {"username": session["username"]}).fetchall()
    return render_template("links.html", links=links, username=session.get("username"))
