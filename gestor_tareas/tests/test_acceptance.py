"""Pruebas de aceptación: recorridos completos de un empleado (flujo de usuario)."""
from .conftest import make_task


def test_flujo_completo_empleado(client, auth):
    """Un empleado se registra, inicia sesión, crea, asigna, completa y elimina tareas."""
    auth.register("supervisor", "sup@plasticos.com")
    auth.register("operario", "op@plasticos.com")

    assert auth.login("supervisor").status_code == 302
    make_task(client, title="Revisar molde 3", assignee="operario", due_date="2026-12-15")
    make_task(client, title="Pedir materia prima")
    pagina = client.get("/").get_data(as_text=True)
    assert "Revisar molde 3" in pagina and "Pedir materia prima" in pagina

    auth.logout()
    auth.login("operario")
    assert "Revisar molde 3" in client.get("/").get_data(as_text=True)
    assert "Pedir materia prima" not in client.get("/").get_data(as_text=True)
    client.post("/tasks/1/toggle")

    auth.logout()
    auth.login("supervisor")
    assert "Revisar molde 3" in client.get("/?status=completed").get_data(as_text=True)
    client.post("/tasks/1/delete")
    assert "Revisar molde 3" not in client.get("/").get_data(as_text=True)


def test_sin_sesion_no_ve_tareas(client):
    response = client.get("/", follow_redirects=True)
    assert "Iniciar sesión" in response.get_data(as_text=True)


def test_estado_vacio(logged_client):
    assert "No hay tareas" in logged_client.get("/").get_data(as_text=True)
