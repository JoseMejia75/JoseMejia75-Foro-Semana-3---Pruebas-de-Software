import os
from flask import Flask
from . import db, auth, tasks, profile


def create_app(test_config=None):
    """Fabrica de la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-cambiar-en-produccion"),
        DATABASE=os.path.join(app.instance_path, "tareas.sqlite"),
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(tasks.bp)
    app.register_blueprint(profile.bp)
    return app
