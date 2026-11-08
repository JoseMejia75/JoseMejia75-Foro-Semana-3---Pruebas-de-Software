from flask import (Blueprint, abort, flash, g, redirect, render_template,
                   request, url_for)

from .auth import login_required
from .db import get_db
from . import validators as v

bp = Blueprint("tasks", __name__)


def get_task(task_id):
    """Devuelve la tarea si existe y el usuario puede verla (dueño o asignado)."""
    task = get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if task is None:
        abort(404)
    if g.user["id"] not in (task["owner_id"], task["assignee_id"]):
        abort(403)
    return task


def get_owned_task(task_id):
    task = get_task(task_id)
    if task["owner_id"] != g.user["id"]:
        abort(403)
    return task


def escape_like(texto):
    """Escapa % y _ para que la búsqueda trate el texto de forma literal."""
    return (texto.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_"))


def resolve_assignee(username):
    """Devuelve (id, error). Vacío = sin asignar."""
    if not username or not username.strip():
        return None, None
    row = get_db().execute("SELECT id FROM users WHERE username = ?",
                           (username.strip(),)).fetchone()
    if row is None:
        return None, "El usuario asignado no existe."
    return row["id"], None


@bp.route("/")
@login_required
def index():
    q = request.args.get("q", "").strip()
    status = request.args.get("status", "all")
    sql = ("SELECT t.*, o.username AS owner_name, a.username AS assignee_name "
           "FROM tasks t JOIN users o ON o.id = t.owner_id "
           "LEFT JOIN users a ON a.id = t.assignee_id "
           "WHERE (t.owner_id = ? OR t.assignee_id = ?)")
    params = [g.user["id"], g.user["id"]]
    if q:
        sql += (" AND (t.title LIKE ? ESCAPE '\\' "
                "OR t.description LIKE ? ESCAPE '\\')")
        patron = "%" + escape_like(q) + "%"
        params += [patron, patron]
    if status == "completed":
        sql += " AND t.completed = 1"
    elif status == "pending":
        sql += " AND t.completed = 0"
    sql += " ORDER BY t.id DESC"
    tasks = get_db().execute(sql, params).fetchall()
    return render_template("index.html", tasks=tasks, q=q, status=status)


@bp.route("/tasks/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date", "").strip()
        assignee_id, a_err = resolve_assignee(request.form.get("assignee", ""))
        error = v.validate_title(title) or v.validate_due_date(due_date) or a_err
        if error:
            flash(error)
        else:
            get_db().execute(
                "INSERT INTO tasks (title, description, due_date, owner_id, assignee_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (title.strip(), description, due_date or None, g.user["id"], assignee_id))
            get_db().commit()
            return redirect(url_for("tasks.index"))
    return render_template("task_form.html", task=None)


@bp.route("/tasks/<int:task_id>/edit", methods=("GET", "POST"))
@login_required
def edit(task_id):
    task = get_owned_task(task_id)
    if request.method == "POST":
        title = request.form.get("title", "")
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date", "").strip()
        assignee_id, a_err = resolve_assignee(request.form.get("assignee", ""))
        error = v.validate_title(title) or v.validate_due_date(due_date) or a_err
        if error:
            flash(error)
        else:
            get_db().execute(
                "UPDATE tasks SET title=?, description=?, due_date=?, assignee_id=? WHERE id=?",
                (title.strip(), description, due_date or None, assignee_id, task_id))
            get_db().commit()
            return redirect(url_for("tasks.index"))
    assignee_name = ""
    if task["assignee_id"]:
        row = get_db().execute("SELECT username FROM users WHERE id = ?",
                               (task["assignee_id"],)).fetchone()
        assignee_name = row["username"] if row else ""
    return render_template("task_form.html", task=task, assignee_name=assignee_name)


@bp.route("/tasks/<int:task_id>/delete", methods=("POST",))
@login_required
def delete(task_id):
    get_owned_task(task_id)
    get_db().execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    get_db().commit()
    return redirect(url_for("tasks.index"))


@bp.route("/tasks/<int:task_id>/toggle", methods=("POST",))
@login_required
def toggle(task_id):
    task = get_task(task_id)
    get_db().execute("UPDATE tasks SET completed = ? WHERE id = ?",
                     (0 if task["completed"] else 1, task_id))
    get_db().commit()
    return redirect(url_for("tasks.index"))
