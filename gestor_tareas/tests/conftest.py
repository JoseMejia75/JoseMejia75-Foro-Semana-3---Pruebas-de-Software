import pytest
from app import create_app


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.sqlite"),
                      "SECRET_KEY": "test"})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def register(self, username="ana", email="ana@correo.com", password="clave1234"):
        return self._client.post("/auth/register", data={
            "username": username, "email": email, "password": password})

    def login(self, username="ana", password="clave1234"):
        return self._client.post("/auth/login", data={
            "username": username, "password": password})

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def logged_client(client, auth):
    auth.register()
    auth.login()
    return client


def make_task(client, title="Revisar máquina", **extra):
    data = {"title": title, "description": "", "due_date": "", "assignee": ""}
    data.update(extra)
    return client.post("/tasks/create", data=data)
