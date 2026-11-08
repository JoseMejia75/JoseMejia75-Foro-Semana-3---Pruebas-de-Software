"""Funciones de validación puras (fáciles de probar con pruebas unitarias)."""
import re
from datetime import datetime

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_username(username):
    if not username or not username.strip():
        return "El nombre de usuario es obligatorio."
    if len(username.strip()) < 3:
        return "El nombre de usuario debe tener al menos 3 caracteres."
    return None


def validate_email(email):
    if not email or not EMAIL_RE.match(email.strip()):
        return "El correo electrónico no es válido."
    return None


def validate_password(password):
    if not password or len(password) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not any(c.isalpha() for c in password) or not any(c.isdigit() for c in password):
        return "La contraseña debe incluir letras y números."
    return None


def validate_title(title):
    if not title or not title.strip():
        return "El título de la tarea es obligatorio."
    if len(title.strip()) > 100:
        return "El título no puede superar los 100 caracteres."
    return None


def validate_due_date(value):
    """La fecha es opcional; si viene, debe ser AAAA-MM-DD."""
    if not value:
        return None
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return "La fecha límite debe tener el formato AAAA-MM-DD."
    return None
