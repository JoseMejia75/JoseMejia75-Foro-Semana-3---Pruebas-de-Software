import functools
import sqlite3
from flask import (Blueprint, flash, g, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from . import validators as v

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        error = (v.validate_username(username) or v.validate_email(email)
                 or v.validate_password(password))
        if error is None:
            try:
                get_db().execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)))
                get_db().commit()
            except sqlite3.IntegrityError:
                error = "Ese usuario o correo ya está registrado."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template("register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Usuario o contraseña incorrectos.")
        else:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("tasks.index"))
    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
