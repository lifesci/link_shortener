from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from sqlalchemy import exc
from app.models import db, Link, UserLink
from app.auth import verify_user
from app.helpers import create_short_link, validate_url
from app.constants import SHORTEN_LINK_RETRY_ATTEMPTS

shorten = Blueprint("shorten", __name__)

@verify_user
@shorten.route('/', methods=["GET", "POST"])
def shortener():
    """Generate short link for URL if one does not already exist.
    If an integrity error occurs, this means that a either short link
    already exists, or there was a collision. In either case, retry a
    fixed number of times. If unsuccessful, send 500.
    """
    if request.method == "POST":
        input_link = request.form.get("link")
        if not validate_url(input_link):
            return "Invalid URL", 400

        attempts = 0
        success = False
        while attempts < SHORTEN_LINK_RETRY_ATTEMPTS:
            attempts += 1
            link = Link.query.get(input_link)
            if not link:
                short_link = create_short_link()
                try:
                    link = Link(long_link = input_link, short_link=short_link)
                    db.session.add(link)
                    db.session.commit()
                except exc.IntegrityError:
                    db.session.rollback()
                    continue

            if session.get("username"):
                try:
                    user_link = UserLink(username=session["username"], long_link = link.long_link)
                    db.session.add(user_link)
                    db.session.commit()
                except exc.IntegrityError:
                    db.session.rollback()

            return { "short_link": link.short_link }

        return "Error shortening link", 500

    return render_template("index.html", username=session.get("username"))

@shorten.route("/<short_link>", methods=["GET"])
def reroute(short_link):
    """Redirect to URL corresponding to short link"""
    link = Link.query.filter_by(short_link=short_link).one_or_none()
    if not link:
        flash("Unable to follow unrecognized short link")
        return redirect(url_for("shorten.shortener"))
    return redirect(link.long_link)
