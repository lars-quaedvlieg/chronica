# app/routes/note_gallery.py
from flask import Blueprint, render_template
from app.services.notes_service import load_notes

bp = Blueprint('note_gallery', __name__, url_prefix='/note_gallery')

@bp.route('/')
def note_gallery():
    # Load notes from the service
    notes = load_notes()
    return render_template('note_gallery.html', notes=notes)
