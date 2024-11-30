from flask import Flask
from .routes import new_entry, note_gallery, view_entry, edit_entry


def create_app():
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(new_entry.bp)
    app.register_blueprint(note_gallery.bp)
    app.register_blueprint(view_entry.bp)
    app.register_blueprint(edit_entry.bp)

    return app
