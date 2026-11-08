"""Pruebas unitarias: funciones de validación (sin Flask ni base de datos)."""
import pytest
from app import validators as v


@pytest.mark.parametrize("value,ok", [("ana", True), ("  ana  ", True), ("", False),
                                      ("   ", False), ("ab", False), (None, False)])
def test_username(value, ok):
    assert (v.validate_username(value) is None) == ok


@pytest.mark.parametrize("value,ok", [("a@b.com", True), ("ana@correo.edu.co", True),
                                      ("sin-arroba.com", False), ("a@b", False),
                                      ("", False), ("a b@c.com", False)])
def test_email(value, ok):
    assert (v.validate_email(value) is None) == ok


@pytest.mark.parametrize("value,ok", [("clave1234", True), ("corta1", False),
                                      ("sololetrasaqui", False), ("12345678", False),
                                      ("", False), (None, False)])
def test_password(value, ok):
    assert (v.validate_password(value) is None) == ok


def test_title_valid_and_invalid():
    assert v.validate_title("Revisar inyectora") is None
    assert v.validate_title("") is not None
    assert v.validate_title("   ") is not None
    assert v.validate_title("x" * 100) is None
    assert v.validate_title("x" * 101) is not None


@pytest.mark.parametrize("value,ok", [("", True), (None, True), ("2026-12-31", True),
                                      ("31-12-2026", False), ("2026-13-45", False),
                                      ("mañana", False)])
def test_due_date(value, ok):
    assert (v.validate_due_date(value) is None) == ok
