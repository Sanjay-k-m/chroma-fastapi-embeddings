from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime, timezone

from app.core.chroma_client import notes_collection
from app.schemas.note_schema import NoteCreate, NoteUpdate


async def list_notes_service():
    """
    Retrieve all stored notes from the vector database.

    Returns:
        dict: A Chroma result object containing ids, documents, and metadata.
    """
    return notes_collection.get()


async def create_note_service(data: NoteCreate, embedding: List[float]) -> str:
    """
    Create a new note and insert it into the vector store.

    Args:
        data (NoteCreate): Title and content of the note.
        embedding (List[float]): Embedding vector generated from the note content.

    Returns:
        str: The UUID of the newly created note.
    """
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
    """
    Update an existing note. If content changes, embedding is updated too.

    Args:
        note_id (str): ID of the note to update.
        data (NoteUpdate): Fields to update (title/content).
        embedding (Optional[List[float]]): New embedding only if content changed.

    Returns:
        str: The updated note's ID.

    Raises:
        ValueError: If the note does not exist.
    """
    result = notes_collection.get(ids=[note_id])
    if not result or not result.get("ids"):
        raise ValueError("Note not found")

    metadatas = result.get("metadatas") or [{}]
    documents: List[str] = result.get("documents") or [""]

    metadata = dict(metadatas[0])
    current_content = documents[0]

    # Merge updates with existing data
    new_content = data.content or current_content
    new_title = data.title or metadata.get("title", "")

    updated_metadata: Dict[str,Any] = {
        **metadata,
        "title": new_title,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    update_params: Dict[str, Any] = {
        "ids": [note_id],
        "documents": [new_content],
        "metadatas": [updated_metadata]
    }

    # Only update embeddings if content changed
    if embedding is not None:
        update_params["embeddings"] = [embedding]

    notes_collection.update(**update_params)
    return note_id


async def delete_note_service(note_id: str) -> None:
    """
    Delete a note from the vector store.

    Args:
        note_id (str): ID of the note to delete.

    Raises:
        ValueError: If the note does not exist.
    """
    result = notes_collection.get(ids=[note_id])
    if not result or not result.get("ids"):
        raise ValueError("Note not found")

    notes_collection.delete(ids=[note_id])
