import sqlite3
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .auth import login_required
from .db import get_db
from . import validators as v

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.route("/", methods=("GET", "POST"))
@login_required
def edit_profile():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        error = v.validate_username(username) or v.validate_email(email)
        if error is None:
            try:
                get_db().execute("UPDATE users SET username=?, email=? WHERE id=?",
                                 (username, email, g.user["id"]))
                get_db().commit()
                flash("Perfil actualizado.")
                return redirect(url_for("profile.edit_profile"))
            except sqlite3.IntegrityError:
                error = "Ese usuario o correo ya está en uso."
        flash(error)
    return render_template("profile.html")


@bp.route("/password", methods=("POST",))
@login_required
def change_password():
    current = request.form.get("current_password", "")
    new = request.form.get("new_password", "")
    if not check_password_hash(g.user["password_hash"], current):
        flash("La contraseña actual no es correcta.")
    elif (err := v.validate_password(new)):
        flash(err)
    else:
        get_db().execute("UPDATE users SET password_hash=? WHERE id=?",
                         (generate_password_hash(new), g.user["id"]))
        get_db().commit()
        flash("Contraseña actualizada.")
    return redirect(url_for("profile.edit_profile"))
