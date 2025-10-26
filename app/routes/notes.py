from datetime import datetime
from typing import Any, List, Optional
from fastapi import APIRouter, HTTPException, status

from app.schemas import Note, NoteCreate, NoteListResponse
from app.schemas.note_update_schema import NoteUpdate
from app.service.note_service import (
    list_notes_service,
    create_note_service,
    update_note_service,
    delete_note_service,
)

notes_route = APIRouter()

def parse_datetime(value: Any) -> Optional[datetime]:
    """Convert stored ISO timestamp string to datetime, return None if invalid."""
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


@notes_route.get(
    "/",
    response_model=NoteListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all notes"
)
async def list_notes() -> NoteListResponse:
    """Return all saved notes."""
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
    summary="Create a new note"
)
async def create_note(item: NoteCreate):
    note_id = await create_note_service(item)
    return {"message": "Note created successfully", "note_id": note_id}


@notes_route.put(
    "/{note_id}",
    status_code=status.HTTP_200_OK,
    summary="Update an existing note"
)
async def update_note(note_id: str, item: NoteUpdate):
    try:
        await update_note_service(note_id, item)
        return {"message": "Note updated successfully", "note_id": note_id}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")


@notes_route.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note"
)
async def delete_note(note_id: str):
    try:
        await delete_note_service(note_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
