# note_update_schema.py
from typing import Optional
from pydantic import BaseModel

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
