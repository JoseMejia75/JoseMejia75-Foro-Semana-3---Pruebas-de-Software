# Sistema de Gestión de Tareas – Plásticos Sustentables

Proyecto del Anexo II (Pruebas de Software y Aseguramiento de Calidad).
Tecnologías: Python 3.12, Flask, SQLite, pytest, pytest-cov, Git/GitHub y GitHub Actions.

## Funcionalidades
- Registro e inicio/cierre de sesión (contraseñas cifradas).
- Crear, editar y eliminar tareas (solo el creador edita o elimina).
- Asignar tareas a un usuario específico (el asignado la ve y la marca completada).
- Filtrar (todas / pendientes / completadas) y buscar por título o descripción.
- Gestión de perfil: editar usuario y correo, cambiar contraseña.

## Cómo ejecutarlo
```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py                    # abre http://127.0.0.1:5000
```

## Cómo correr las pruebas
```bash
pytest --cov=app --cov-report=term-missing
```

## Estructura
```
app/            código fuente (auth, tasks, profile, validators, db, templates)
tests/          pruebas unitarias, de integración, de aceptación y de regresión
docs/           casos de prueba e informe final
.github/workflows/tests.yml   ejecución automática de pruebas en GitHub Actions
```

## Subirlo a GitHub
```bash
git init
git add .
git commit -m "Sistema de gestión de tareas con pruebas"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/gestor-tareas.git
git push -u origin main
```
