from flask import Blueprint, render_template

bp = Blueprint('view_entry', __name__, url_prefix='/view_entry')

@bp.route('/<int:entry_id>')
def view_entry(entry_id):
    # Logic for viewing a specific entry
    entry = {'id': entry_id, 'title': 'Sample Entry', 'content': 'This is a sample entry content.'}
    return render_template('view_entry.html', entry=entry)
