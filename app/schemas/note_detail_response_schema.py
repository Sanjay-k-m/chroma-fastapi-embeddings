# note_detail_response_schema.py
from pydantic import BaseModel
from .note_schema import Note

class NoteDetailResponse(BaseModel):
    message: str
    note: Note
