from typing import List
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
client = genai.Client(api_key=os.getenv("GEN_API_KEY"))

def embed_text(text: str) -> List[float]:
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )

    # Safely get first embedding values
    if response.embeddings and response.embeddings[0].values:
#         print(list(response.embeddings[0].values)
# )
        return list(response.embeddings[0].values)

    raise ValueError("No embedding values returned from model")
