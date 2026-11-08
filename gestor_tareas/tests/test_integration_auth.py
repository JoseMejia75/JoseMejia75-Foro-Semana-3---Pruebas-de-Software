"""Pruebas de integración: registro, inicio de sesión y base de datos."""
from app.db import get_db


def test_register_page_loads(client):
    assert client.get("/auth/register").status_code == 200


def test_register_creates_user_with_hashed_password(client, app):
    response = client.post("/auth/register", data={
        "username": "ana", "email": "Ana@Correo.com", "password": "clave1234"})
    assert response.status_code == 302
    with app.app_context():
        user = get_db().execute("SELECT * FROM users WHERE username='ana'").fetchone()
        assert user is not None
        assert user["email"] == "ana@correo.com"
        assert user["password_hash"] != "clave1234"


def test_register_duplicate_user(client, auth):
    auth.register()
    response = auth.register(email="otro@correo.com")
    assert "ya está registrado" in response.get_data(as_text=True)


def test_register_duplicate_email(client, auth):
    auth.register()
    response = auth.register(username="luis")
    assert "ya está registrado" in response.get_data(as_text=True)


def test_register_invalid_data(client):
    cases = [
        ({"username": "", "email": "a@b.com", "password": "clave1234"}, "obligatorio"),
        ({"username": "ana", "email": "mal", "password": "clave1234"}, "no es válido"),
        ({"username": "ana", "email": "a@b.com", "password": "123"}, "al menos 8"),
    ]
    for data, msg in cases:
        response = client.post("/auth/register", data=data)
        assert msg in response.get_data(as_text=True)


def test_login_ok_redirects_to_tasks(client, auth):
    auth.register()
    response = auth.login()
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_login_wrong_password(client, auth):
    auth.register()
    response = auth.login(password="incorrecta1")
    assert "incorrectos" in response.get_data(as_text=True)


def test_login_unknown_user(client):
    response = client.post("/auth/login", data={"username": "nadie", "password": "x"})
    assert "incorrectos" in response.get_data(as_text=True)


def test_logout_blocks_access(client, auth):
    auth.register()
    auth.login()
    auth.logout()
    response = client.get("/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_protected_routes_require_login(client):
    for path in ["/", "/tasks/create", "/profile/"]:
        response = client.get(path)
        assert response.status_code == 302
        assert "/auth/login" in response.headers["Location"]
