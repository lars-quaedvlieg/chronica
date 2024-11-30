from app.services.notes_service import load_all_notes


def semantic_search_notes(query):
    """
    Perform a semantic search on the saved notes based on the query.

    Args:
        query (str): The search query.

    Returns:
        list: A list of matching notes.
    """
    # Placeholder logic for semantic search
    # In practice, you'd use a proper model like a RAG pipeline, or a semantic search tool like FAISS or ElasticSearch.

    # Load all notes
    notes = load_all_notes()

    # Simple keyword-based semantic matching placeholder
    matching_notes = []
    for note in notes:
        if query.lower() in note['title'].lower() or query.lower() in note['summary'].lower() or query.lower() in note[
            'transcription'].lower():
            matching_notes.append(note)

    return matching_notes