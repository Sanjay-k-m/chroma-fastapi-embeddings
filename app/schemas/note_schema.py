from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# ---- Base Metadata ----
class NoteMetadata(BaseModel):
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ---- Core Note Model ----
class Note(BaseModel):
    id: str
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ---- Create Note ----
class NoteCreate(BaseModel):
    title: str
    content: str


# ---- Update Note ----
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


# ---- Search Result ----
class NoteSearchResult(BaseModel):
    id: str
    content: str
    score: float
    metadata: Optional[NoteMetadata] = None


# ---- List Notes Response ----
class NoteListResponse(BaseModel):
    message: str
    notes: List[Note]


# ---- Single Note Detail Response ----
class NoteDetailResponse(BaseModel):
    message: str
    note: Note
