from datetime import datetime
from typing import Optional
from app.schemas.note_create_schema import NoteCreate

class Note(NoteCreate):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
