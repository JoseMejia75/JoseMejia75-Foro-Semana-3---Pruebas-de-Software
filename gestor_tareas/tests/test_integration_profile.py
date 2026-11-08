"""Pruebas de integración: gestión del perfil y cambio de contraseña."""


def test_edit_profile(logged_client):
    logged_client.post("/profile/", data={"username": "ana2", "email": "nuevo@correo.com"})
    assert "ana2" in logged_client.get("/profile/").get_data(as_text=True)


def test_edit_profile_invalid_email(logged_client):
    response = logged_client.post("/profile/", data={"username": "ana", "email": "mal"})
    assert "no es válido" in response.get_data(as_text=True)


def test_edit_profile_duplicate_username(client, auth):
    auth.register("ana", "ana@correo.com")
    auth.register("luis", "luis@correo.com")
    auth.login("luis")
    response = client.post("/profile/", data={"username": "ana", "email": "luis@correo.com"})
    assert "ya está en uso" in response.get_data(as_text=True)


def test_change_password_and_login_with_new(client, auth):
    auth.register()
    auth.login()
    client.post("/profile/password", data={
        "current_password": "clave1234", "new_password": "nueva5678"})
    auth.logout()
    assert "incorrectos" in auth.login(password="clave1234").get_data(as_text=True)
    assert auth.login(password="nueva5678").status_code == 302


def test_change_password_wrong_current(logged_client):
    response = logged_client.post("/profile/password", data={
        "current_password": "mala", "new_password": "nueva5678"}, follow_redirects=True)
    assert "no es correcta" in response.get_data(as_text=True)


def test_change_password_weak_new(logged_client):
    response = logged_client.post("/profile/password", data={
        "current_password": "clave1234", "new_password": "123"}, follow_redirects=True)
    assert "al menos 8" in response.get_data(as_text=True)
