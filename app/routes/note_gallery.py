# app/routes/note_gallery.py
from flask import Blueprint, render_template, request, jsonify
from app.services.notes_service import load_notes, load_all_notes
from app.services.semantic_search_service import semantic_search_notes
from app.services.rag_service import get_rag_summary
from app.services.tags_service import get_all_available_tags

bp = Blueprint('note_gallery', __name__, url_prefix='/note_gallery')

@bp.route('/')
def note_gallery():
    # Load notes from the service
    notes = load_notes()
    all_available_tags = get_all_available_tags()
    return render_template('note_gallery.html', notes=notes, all_available_tags=all_available_tags)

@bp.route('/semantic_search', methods=['POST'])
def semantic_search():
    # Parse the incoming JSON data
    data = request.get_json()

    # Validate that 'query' is present in the data
    if not data or 'query' not in data:
        return jsonify({'error': 'Missing search query'}), 400

    # Extract the search query
    query = data['query']

    if len(query) == 0:
        matching_notes = load_all_notes()
    else:
        # Call the semantic search service to find matching notes
        matching_notes = semantic_search_notes(query)

    print(matching_notes)

    return jsonify({'notes': matching_notes}), 200


@bp.route('/rag_summary', methods=['POST'])
def rag_summary():
    # Parse the incoming JSON data
    data = request.get_json()

    # Validate that 'query' is present in the data
    if not data or 'query' not in data:
        return jsonify({'error': 'Missing search query'}), 400

    # Extract the search query
    query = data['query']

    if len(query) == 0:
        matching_notes = load_all_notes()
        summary = ""
    else:
        # Call the semantic search service to find matching notes
        summary, matching_notes = get_rag_summary(query)

    print(matching_notes, summary)

    return jsonify({'relevant_notes': matching_notes, 'summary': summary}), 200