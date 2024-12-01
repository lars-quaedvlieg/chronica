from app.services.notes_service import load_all_notes


def semantic_search_notes(query):
    """
    Perform a semantic search on the saved notes based on the query.

    Args:
        query (str): The search query.

    Returns:
        list: A list of matching notes.
    """
    # In practice, you'd use a proper model like a RAG pipeline, or a semantic search tool like FAISS or ElasticSearch.

    hits = client.query_points(
        collection_name=collection_name,
        query=encoder.encode(query).tolist(),
        limit=5,
    ).points

    matching_ids = [hit.id for hit in hits]
    matching_notes = load_note_ids(matching_ids)

    return matching_notes