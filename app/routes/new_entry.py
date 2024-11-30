import datetime
import json
import os

from flask import Blueprint, render_template, request, jsonify

from app.services import transcription
from app.services.transcription_information import get_title_summary_tags_from_transcription

NOTES_DIR = 'notes'

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

    # Extract the title, summary, and tags from the transcription
    title, summary, tags = get_title_summary_tags_from_transcription(transcription)

    # Generate a unique note ID using the current timestamp (as an integer)
    current_time = datetime.datetime.now()
    note_id = str(int(current_time.timestamp()))

    # Create a human-readable datetime string
    datetime_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

    # Create a directory to store the note
    save_path = os.path.join(NOTES_DIR, note_id)
    os.makedirs(save_path, exist_ok=True)

    # Save the JSON metadata
    json_dict = {
        'id': note_id,
        'title': title,
        'summary': summary,
        'tags': tags,
        'transcription': transcription,
        'datetime': datetime_str
    }
    json_path = os.path.join(save_path, f'{note_id}.json')
    with open(json_path, 'w') as json_file:
        json.dump(json_dict, json_file, indent=4)

    # Save the audio data
    audio_path = os.path.join(save_path, f'{note_id}.wav')
    audio_data.save(audio_path)

    # Additional logic such as saving to a database can be added here

    return jsonify({'message': 'Entry saved successfully'}), 200