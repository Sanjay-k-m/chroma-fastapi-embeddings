from typing import List
from app.core.embeddings import embed_text
from app.core.chroma_client import notes_collection
from app.utils.datetime_utils import parse_datetime
from app.schemas.note_schema import NoteMetadata, NoteSearchResult


async def search_notes_service(query: str, top_k: int = 5) -> List[NoteSearchResult]:
    """
    Perform semantic search on saved notes.

    This function converts the input query text into an embedding vector,
    performs a nearest-neighbor similarity search in the Chroma vector store,
    and returns the top matched notes ordered by semantic relevance.

    Args:
        query (str): The search phrase to match against note content.
        top_k (int): Number of most relevant notes to return. Defaults to 5.

    Returns:
        List[NoteSearchResult]: A list of search results including note content,
        score, and metadata such as title and timestamps.
    """
    query_embedding = embed_text(query)

    results = notes_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    ) or {}

    ids = (results.get("ids") or [[]])[0]
    docs = (results.get("documents") or [[]])[0]
    scores = (results.get("distances") or [[]])[0]
    metas = (results.get("metadatas") or [[]])[0]

    matches: List[NoteSearchResult] = []

    for id_, doc, score, meta in zip(ids, docs, scores, metas):
        metadata = None

        if isinstance(meta, dict):
            metadata = NoteMetadata(
                title=str(meta.get("title")),
                created_at=parse_datetime(meta.get("created_at")),
                updated_at=parse_datetime(meta.get("updated_at"))
            )

        matches.append(
            NoteSearchResult(
                id=id_,
                content=doc,
                score=score,
                metadata=metadata
            )
        )

    return matches
