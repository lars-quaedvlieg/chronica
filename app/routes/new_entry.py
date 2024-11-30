from flask import Blueprint, render_template, request, jsonify

from app.services import transcription

bp = Blueprint('new_entry', __name__, url_prefix='/new_entry')

@bp.route('/', methods=['GET'])
def new_entry():
    return render_template('new_entry.html')

@bp.route('/stream_audio', methods=['POST'])
def stream_audio():
    audio_data = request.files['audio']
    # Process the audio using the transcription service
    transcript_chunk = transcription.process_audio(audio_data)
    return jsonify({'transcription': transcript_chunk})

@bp.route('/save_entry', methods=['POST'])
def save_entry():
    if 'audio' not in request.files or 'transcription' not in request.form:
        return jsonify({'error': 'Missing audio or transcription data'}), 400

    audio_data = request.files['audio']
    transcription = request.form['transcription']

    print(audio_data, transcription)

    # You can implement additional saving logic here if needed, such as saving to a database
    return jsonify({'message': 'Entry saved in session'}), 200