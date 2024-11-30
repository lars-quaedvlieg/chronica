# app/routes/home.py
from flask import Blueprint, render_template

from app.services.notes_service import load_most_recent_k_notes

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def home():
    # Load the most recent 3 notes (or however many you want to display)
    recent_notes = load_most_recent_k_notes(3)

    # Logic for handling the home page
    return render_template('home.html', recent_notes=recent_notes)