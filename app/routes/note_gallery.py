from flask import Blueprint, render_template

bp = Blueprint('note_gallery', __name__, url_prefix='/note_gallery')

@bp.route('/')
def note_gallery():
    # Logic for displaying notes
    notes = [
        {'title': 'February Note 1', 'content': 'Sample content for February note 1'},
        {'title': 'January Note 1', 'content': 'Sample content for January note 1'}
    ]
    return render_template('note_gallery.html', notes=notes)