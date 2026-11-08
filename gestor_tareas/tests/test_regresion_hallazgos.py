"""Pruebas de regresión de los defectos encontrados durante las pruebas exploratorias."""
from .conftest import make_task


def _dos_usuarios(client, auth):
    auth.register("ana", "ana@correo.com")
    auth.register("luis", "luis@correo.com")
    auth.login("ana")


def test_hallazgo_01_editar_conserva_asignado(client, auth):
    """DEF-01: al abrir el formulario de edición, el campo 'Asignar a' debe mostrar
    el usuario ya asignado; si no, al guardar se pierde la asignación."""
    _dos_usuarios(client, auth)
    make_task(client, title="Revisar molde", assignee="luis")
    formulario = client.get("/tasks/1/edit").get_data(as_text=True)
    assert 'value="luis"' in formulario


def test_hallazgo_02_busqueda_no_trata_comodines_como_patron(client, auth):
    """DEF-02: buscar '%' o '_' debe buscar ese texto literal, no devolver todo."""
    _dos_usuarios(client, auth)
    make_task(client, title="Tarea normal")
    make_task(client, title="Avance 100% listo")
    resultado = client.get("/?q=%25").get_data(as_text=True)
    assert "Avance 100% listo" in resultado
    assert "Tarea normal" not in resultado
