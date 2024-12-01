from app.services.notes_service import load_all_notes, load_note_ids
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


collection_name = "journal_notes"
client = QdrantClient("http://localhost:6333")
encoder = SentenceTransformer("BAAI/bge-base-en-v1.5")

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