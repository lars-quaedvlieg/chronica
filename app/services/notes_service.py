import json
import os
from datetime import datetime

NOTES_DIR = 'app/static/notes'

def load_notes(note_ids=None):
    """
    Load notes based on the given note IDs or load all notes if no IDs are specified.
    """
    if note_ids is None:
        notes = load_all_notes()
    else:
        notes = load_note_ids(note_ids)
    return notes


def load_most_recent_k_notes(k):
    """
    Load the most recent k notes based on datetime.
    """
    notes = []

    # Iterate over each note directory
    if os.path.exists(NOTES_DIR):
        for note_id in os.listdir(NOTES_DIR):
            note_dir = os.path.join(NOTES_DIR, note_id)
            json_path = os.path.join(note_dir, f'data.json')

            if os.path.isdir(note_dir) and os.path.exists(json_path):
                # Read the note data from the JSON file
                with open(json_path, 'r') as json_file:
                    note = json.load(json_file)
                    # Parse the datetime for sorting later
                    note['parsed_datetime'] = datetime.fromisoformat(note['datetime'])
                    notes.append(note)

    # Sort notes by parsed datetime in descending order (most recent first)
    sorted_notes = sorted(notes, key=lambda x: x['parsed_datetime'], reverse=True)

    # Return the top k notes (or fewer if there are not enough notes)
    return sorted_notes[:k]


def load_note_ids(note_ids):
    """
    Load specific notes based on a list of note IDs.
    """
    notes = []
    for note_id in note_ids:
        note_path = os.path.join(NOTES_DIR, str(note_id), f'data.json')
        if os.path.exists(note_path):
            with open(note_path, 'r') as json_file:
                note = json.load(json_file)
                notes.append(note)
    return notes


def load_all_notes():
    """
    Load all notes by reading each JSON file in the NOTES_DIR.
    """
    notes = []
    if os.path.exists(NOTES_DIR):
        for note_id in os.listdir(NOTES_DIR):
            note_dir = os.path.join(NOTES_DIR, note_id)
            json_path = os.path.join(note_dir, f'data.json')
            if os.path.isdir(note_dir) and os.path.exists(json_path):
                with open(json_path, 'r') as json_file:
                    note = json.load(json_file)
                    notes.append(note)
    return notes
