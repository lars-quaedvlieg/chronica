import os
import json

from app.routes.new_entry import NOTES_DIR


def load_notes(note_ids=None):
    """
    Load notes based on the given note IDs or load all notes if no IDs are specified.
    """
    if note_ids is None:
        notes = load_all_notes()
    else:
        notes = load_note_ids(note_ids)
    return notes


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
