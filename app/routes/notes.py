from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, status

from app.core.embeddings import embed_text
from app.schemas.note_schema import Note, NoteCreate, NoteListResponse, NoteUpdate
from app.service.note_service import (
    list_notes_service,
    create_note_service,
    update_note_service,
    delete_note_service,
)
from app.service.search_service import search_notes_service
from app.utils.datetime_utils import parse_datetime

notes_route = APIRouter()


@notes_route.get(
    "/",
    response_model=NoteListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all notes",
    description="Fetch and return all saved notes including their metadata and timestamps.",
)
async def list_notes() -> NoteListResponse:
    """
    Retrieve all notes stored in the system.

    Returns:
        A list of notes containing ID, title, content, created_at, and updated_at fields.
    """
    result = await list_notes_service()

    ids = result.get("ids") or []
    documents = result.get("documents") or []
    metadatas = result.get("metadatas") or []

    notes: List[Note] = []

    for i, note_id in enumerate(ids):
        metadata = metadatas[i] or {}
        notes.append(
            Note(
                id=str(note_id),
                title=str(metadata.get("title", "")),
                content=documents[i],
                created_at=parse_datetime(metadata.get("created_at")),
                updated_at=parse_datetime(metadata.get("updated_at")),
            )
        )

    return NoteListResponse(message="Notes fetched successfully", notes=notes)


@notes_route.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Create a new note",
    description="Create and save a new note with text embedding for semantic search.",
)
async def create_note(item: NoteCreate):
    """
    Create a note and generate an embedding for semantic search.

    Args:
        item: NoteCreate schema containing `title` and `content`.

    Returns:
        Newly created note ID with success message.
    """
    embedding = embed_text(item.content)
    note_id = await create_note_service(item, embedding)
    return {"message": "Note created successfully", "note_id": note_id}


@notes_route.put(
    "/{note_id}",
    status_code=status.HTTP_200_OK,
    summary="Update an existing note",
    description="Update an existing note. Embedding is regenerated only if content is changed.",
)
async def update_note(note_id: str, item: NoteUpdate):
    """
    Update an existing note.

    Args:
        note_id: ID of the note to update.
        item: NoteUpdate schema with optional title/content changes.

    Returns:
        Success message with ID of updated note.
    """
    try:
        embedding = None

        if item.content is not None and item.content.strip() != "":
            embedding = embed_text(item.content)

        await update_note_service(note_id, item, embedding)
        return {"message": "Note updated successfully", "note_id": note_id}

    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@notes_route.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note permanently by its unique ID.",
)
async def delete_note(note_id: str):
    """
    Delete a note by ID.

    Args:
        note_id: ID of the note to delete.
    """
    try:
        await delete_note_service(note_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@notes_route.get(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Semantic search notes",
    description="Perform vector similarity search across all notes based on meaning.",
)
async def search_notes(q: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Perform semantic search on notes based on the meaning of the query text.

    Args:
        q: The text query to search for.
        top_k: Number of results to return (default=5).

    Returns:
        List of notes ranked by semantic relevance.
    """
    results: List[Any] = await search_notes_service(q, top_k)
    return {"message": "Search results", "results": results}
