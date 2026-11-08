"""Pruebas de integración: CRUD de tareas, asignación, filtros y autorización."""
from app.db import get_db
from .conftest import make_task


def count_tasks(app):
    with app.app_context():
        return get_db().execute("SELECT COUNT(*) FROM tasks").fetchone()[0]


def test_create_task(logged_client, app):
    response = make_task(logged_client, due_date="2026-12-01")
    assert response.status_code == 302
    assert count_tasks(app) == 1
    assert "Revisar máquina" in logged_client.get("/").get_data(as_text=True)


def test_create_task_without_title_is_rejected(logged_client, app):
    response = make_task(logged_client, title="")
    assert "obligatorio" in response.get_data(as_text=True)
    assert count_tasks(app) == 0


def test_create_task_bad_date(logged_client, app):
    response = make_task(logged_client, due_date="31/12/2026")
    assert "formato" in response.get_data(as_text=True)
    assert count_tasks(app) == 0


def test_edit_task(logged_client, app):
    make_task(logged_client)
    logged_client.post("/tasks/1/edit", data={
        "title": "Título nuevo", "description": "d", "due_date": "", "assignee": ""})
    assert "Título nuevo" in logged_client.get("/").get_data(as_text=True)


def test_edit_form_prefilled(logged_client):
    make_task(logged_client, title="Soldar pieza")
    assert "Soldar pieza" in logged_client.get("/tasks/1/edit").get_data(as_text=True)


def test_delete_task(logged_client, app):
    make_task(logged_client)
    logged_client.post("/tasks/1/delete")
    assert count_tasks(app) == 0


def test_missing_task_returns_404(logged_client):
    assert logged_client.get("/tasks/999/edit").status_code == 404
    assert logged_client.post("/tasks/999/delete").status_code == 404


def test_toggle_completed_and_filters(logged_client):
    make_task(logged_client, title="Tarea pendiente")
    make_task(logged_client, title="Tarea hecha")
    logged_client.post("/tasks/2/toggle")
    done = logged_client.get("/?status=completed").get_data(as_text=True)
    pending = logged_client.get("/?status=pending").get_data(as_text=True)
    assert "Tarea hecha" in done and "Tarea pendiente" not in done
    assert "Tarea pendiente" in pending and "Tarea hecha" not in pending


def test_search_tasks(logged_client):
    make_task(logged_client, title="Mantenimiento inyectora")
    make_task(logged_client, title="Limpiar bodega", description="reciclaje de plástico")
    by_title = logged_client.get("/?q=inyectora").get_data(as_text=True)
    by_desc = logged_client.get("/?q=reciclaje").get_data(as_text=True)
    assert "Mantenimiento inyectora" in by_title and "Limpiar bodega" not in by_title
    assert "Limpiar bodega" in by_desc


def test_assign_to_unknown_user_fails(logged_client, app):
    response = make_task(logged_client, assignee="fantasma")
    assert "no existe" in response.get_data(as_text=True)
    assert count_tasks(app) == 0


def test_assigned_user_sees_and_completes_task(client, auth):
    auth.register("ana", "ana@correo.com")
    auth.register("luis", "luis@correo.com")
    auth.login("ana")
    make_task(client, title="Empacar pedido", assignee="luis")
    auth.logout()
    auth.login("luis")
    assert "Empacar pedido" in client.get("/").get_data(as_text=True)
    assert client.post("/tasks/1/toggle").status_code == 302
    assert "Empacar pedido" in client.get("/?status=completed").get_data(as_text=True)


def test_assignee_cannot_edit_or_delete(client, auth):
    auth.register("ana", "ana@correo.com")
    auth.register("luis", "luis@correo.com")
    auth.login("ana")
    make_task(client, assignee="luis")
    auth.logout()
    auth.login("luis")
    assert client.get("/tasks/1/edit").status_code == 403
    assert client.post("/tasks/1/delete").status_code == 403


def test_user_cannot_touch_other_users_tasks(client, auth):
    auth.register("ana", "ana@correo.com")
    auth.register("luis", "luis@correo.com")
    auth.login("ana")
    make_task(client, title="Privada de Ana")
    auth.logout()
    auth.login("luis")
    assert "Privada de Ana" not in client.get("/").get_data(as_text=True)
    assert client.get("/tasks/1/edit").status_code == 403
    assert client.post("/tasks/1/toggle").status_code == 403
    assert client.post("/tasks/1/delete").status_code == 403
