# note_list_response_schema.py
from pydantic import BaseModel
from typing import List
from .note_schema import Note

class NoteListResponse(BaseModel):
    message: str
    notes: List[Note]
