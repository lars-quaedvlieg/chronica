from flask import Blueprint, render_template, request
from ..services.transcription import transcribe_audio

bp = Blueprint('new_entry', __name__, url_prefix='/new_entry')

@bp.route('/', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        # Logic for handling live transcription
        audio_file = request.files['audio']
        transcript = transcribe_audio(audio_file)
        return render_template('new_entry.html', transcript=transcript)
    return render_template('new_entry.html')