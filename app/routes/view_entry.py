# app/routes/view_entry.py
from flask import Blueprint, render_template, request
from app.services.notes_service import load_notes

bp = Blueprint('view_entry', __name__, url_prefix='/view_entry')


@bp.route('/<int:note_id>')
def view_entry(note_id):
    # Load notes from the service and find the note by ID
    notes = load_notes()
    note = next((note for note in notes if note['id'] == note_id), None)

    if not note:
        return "Note not found", 404

    return render_template('view_entry.html', note=note)
