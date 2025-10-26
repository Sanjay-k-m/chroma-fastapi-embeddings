from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime, timezone
from app.core.chroma_client import notes_collection
from app.schemas.note_schema import NoteCreate, NoteUpdate


async def list_notes_service():
    return notes_collection.get()


async def create_note_service(data: NoteCreate, embedding: List[float]) -> str:
    note_id = str(uuid4())
    now = datetime.now(timezone.utc).isoformat()

    notes_collection.add(
        ids=[note_id],
        documents=[data.content],
        metadatas=[{
            "title": data.title,
            "created_at": now,
            "updated_at": now
        }],
        embeddings=[embedding]
    )
    return note_id


async def update_note_service(note_id: str, data: NoteUpdate, embedding: Optional[List[float]]) -> str:
    """Update a note and optionally update embedding if content changed."""
    
    result = notes_collection.get(ids=[note_id])
    if not result or not result.get("ids"):
        raise ValueError("Note not found")

    metadatas = result.get("metadatas") or [{}]
    documents: List[str] = result.get("documents") or [""]

    metadata = dict(metadatas[0])
    current_content = documents[0]

    new_content = data.content if data.content is not None else current_content
    new_title = data.title if data.title is not None else metadata.get("title", "")

    updated_metadata: Dict[str, Any] = {
        **metadata,
        "title": new_title,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    update_params : Dict[str,Any] = {
        "ids": [note_id],
        "documents": [new_content],
        "metadatas": [updated_metadata]
    }

    # ✅ Only update embeddings if content changed (embedding provided)
    if embedding is not None:
        update_params["embeddings"] = [embedding]

    notes_collection.update(**update_params)

    return note_id


async def delete_note_service(note_id: str) -> None:
    result = notes_collection.get(ids=[note_id])
    if not result or not result.get("ids"):
        raise ValueError("Note not found")

    notes_collection.delete(ids=[note_id])
