# app/routes/home.py
from flask import Blueprint, render_template, jsonify, send_file

from app.services.notes_service import load_most_recent_k_notes
from app.services.word_frequencies import generate_wordcloud

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def home():
    # Load the most recent 3 notes (or however many you want to display)
    recent_notes = load_most_recent_k_notes(3)

    # Logic for handling the home page
    return render_template('home.html', recent_notes=recent_notes)

@bp.route('/wordcloud', methods=['GET'])
def wordcloud():
    try:
        # Generate the word cloud image
        wordcloud_path = generate_wordcloud()

        # Serve the generated word cloud image
        return send_file(wordcloud_path, mimetype='image/png')
    except Exception as e:
        return jsonify({'error': str(e)}), 500