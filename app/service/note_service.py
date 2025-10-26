from typing import Any, Dict, Sequence
from uuid import uuid4
from datetime import datetime, timezone
from app.core.chroma_client import notes_collection
from app.schemas import NoteCreate,NoteUpdate

async def list_notes_service():
    return notes_collection.get()




async def create_note_service(data: NoteCreate) -> str:
    note_id = str(uuid4())
    now = datetime.now().isoformat()

    notes_collection.add(
        ids=[note_id],
        documents=[data.content],
        metadatas=[{
            "title": data.title,
            "created_at": now,
            "updated_at": now
        }]
    )

    return note_id


async def update_note_service(note_id: str, data: NoteUpdate) -> str:
    """Update only the fields provided in the NoteUpdate payload."""

    result = notes_collection.get(ids=[note_id])

    if not result or not result.get("ids"):
        raise ValueError("Note not found")

    metadatas: Sequence[Any] = result.get("metadatas") or [{}]
    documents: Sequence[Any] = result.get("documents") or [""]

    # ✅ Convert metadata to dict safely
    metadata = dict(metadatas[0]) if metadatas[0] else {}
    current_content = str(documents[0]) if documents[0] else ""

    new_content = data.content if data.content is not None else current_content
    new_title = data.title if data.title is not None else metadata.get("title", "")

    updated_metadata : Dict[str,Any] = {
        **metadata,  # <--- THIS means "copy metadata and overwrite keys below"
        "title": new_title,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    notes_collection.update(
        ids=[note_id],
        documents=[new_content],
        metadatas=[updated_metadata]
    )

    return note_id



async def delete_note_service(note_id: str) -> None:
    """Delete a note by ID."""
    
    # Check if note exists
    result = notes_collection.get(ids=[note_id])
    if not result or not result.get("ids"):
        raise ValueError("Note not found")

    # Perform delete
    notes_collection.delete(ids=[note_id])
