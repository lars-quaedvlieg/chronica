from app.services.notes_service import load_all_notes


def get_rag_summary(query):
    """
    Perform a retrieval augmented generation for the query using the saved notes as context.

    Args:
        query (str): The search query.

    Returns:
        Tuple[str, list]: Tuple of the summary + a list of relevant notes.
    """
    # Placeholder logic for rag

    # Load all notes
    notes = load_all_notes()

    # Simple keyword-based semantic matching placeholder
    relevant_notes = []
    for note in notes:
        if not query.lower() in note['title'].lower() and not query.lower() in note['summary'].lower() and not query.lower() in note[
            'transcription'].lower():
            relevant_notes.append(note)
    summary = f"the summary for the query '{query}' is this"

    print(summary, relevant_notes)

    return summary, relevant_notes