# core/chroma_client.py
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings()
)

notes_collection = client.get_or_create_collection("notes")
