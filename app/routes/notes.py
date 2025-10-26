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

# from  app.core.search_engine import chroma_search

notes_route = APIRouter()

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
    embedding = embed_text(item.content)   # ✅ embedding done here
    note_id = await create_note_service(item,embedding)
    return {"message": "Note created successfully", "note_id": note_id}


@notes_route.put(
    "/{note_id}",
    status_code=status.HTTP_200_OK,
    summary="Update an existing note"
)
async def update_note(note_id: str, item: NoteUpdate):
    try:
        embedding = None
        
        # Generate embedding only if content is updated
        if item.content is not None and item.content.strip() != "":
            embedding = embed_text(item.content)

        await update_note_service(note_id, item, embedding=embedding)
        return {"message": "Note updated successfully", "note_id": note_id}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )


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



@notes_route.get(
    "/search",
    status_code=status.HTTP_200_OK,
    summary="Semantic search notes"
)
async def search_notes(q: str, top_k: int = 5)->Dict[str,Any]:
    results:List[Any] = await search_notes_service(q, top_k)
    return {
        "message": "Search results",
        "results": results
    }