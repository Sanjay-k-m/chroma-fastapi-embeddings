
from typing import List
from app.core.embeddings import embed_text
from app.core.chroma_client import notes_collection
from app.routes.notes import parse_datetime
from app.schemas.note_schema import NoteMetadata, NoteSearchResult


async def search_notes_service(query: str, top_k: int = 5) -> List[NoteSearchResult]:
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
                id=str(id_),
                content=str(doc),
                score=float(score),
                metadata=metadata
            )
        )

    return matches
