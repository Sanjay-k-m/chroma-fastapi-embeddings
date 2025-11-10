A **production-ready**, minimal API using **FastAPI + ChromaDB + Gemini 2.5 Flash**

**No tags • No filters • No bloat** — intentionally simple so you **understand vector search in 10 minutes**

![Semantic Search Demo](https://raw.githubusercontent.com/Sanjay-k-m/chroma-fastapi-embeddings/main/demo.gif)

---

## Live Working Example (Try Right Now!)

```text
http://localhost:8000/search?q=What%20words%20refer%20to%20transportation%20vehicles%20that%20travel%20on%20land%2C%20water%2C%20or%20air%3F&top_k=5
Result: Instantly returns notes about cars, ships, airplanes with 97%+ similarity scores

Features

Add plain text notes
Semantic search (understands meaning, not just keywords)
Delete & list notes
Persistent storage (chromadb/ folder)
Powered by Gemini 2.5 Flash (fastest free embedding model)
400+ dummy notes via one-click bulk import
Clean, modular code (ready for production)


Tech Stack

ToolWhy It's PerfectFastAPIBlazing fast + auto Swagger UIChromaDBLocal, persistent, zero-configGemini 2.5 FlashFree, fast, 1M tokens/monthPython 3.11+Works everywhere

Quick Start (2 Minutes)
bashgit clone https://github.com/Sanjay-k-m/chroma-fastapi-embeddings.git
cd chroma-fastapi-embeddings

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Get FREE Gemini API key (30 seconds)
# → https://aistudio.google.com/app/apikey
cp .env.example .env
echo "GEMINI_API_KEY=your_key_here" > .env

# Optional: Load 400+ dummy notes instantly
python app/scripts/bulk_import.py

uvicorn app.main:app --reload
Open Swagger UI → http://localhost:8000/docs

Bulk Import 400+ Dummy Notes (One Command)
bashpython app/scripts/bulk_import.py
→ Adds real-world notes about AI, vehicles, food, tech, science, history
→ Perfect for instant testing and demo videos

API Endpoints
MethodEndpointDescriptionPOST/notes/Add a noteGET/notes/List all notesDELETE/notes/{id}Delete noteGET/search?q=...&top_k=nSemantic search
Search Explained: top_k Parameter

top_k=5 → Return top 5 most similar notes
top_k=1 → Return only the best match
Default: top_k=5

Example (Copy-Paste):
textGET /search?q=What words refer to transportation vehicles that travel on land, water, or air?&top_k=5
Sample Response:
json{
  "results": [
    {
      "id": "a1b2c3d4",
      "content": "Cars, buses, trains travel on land. Ships and boats on water. Airplanes and helicopters in air.",
      "score": 0.974
    },
    { "id": "e5f6g7h8", "content": "...", "score": 0.892 }
  ]
}

Project Structure
text└── app
    ├── core
    │   ├── chroma_client.py
    │   ├── embeddings.py        ← Gemini 2.5 Flash
    │   ├── exceptions.py
    │   └── logger.py
    ├── routes
    │   └── notes.py             ← All endpoints
    ├── schemas
    │   └── note_schema.py
    ├── scripts
    │   └── bulk_import.py       ← 400+ dummy notes
    ├── service
    │   ├── note_service.py
    │   └── search_service.py
    ├── utils
    │   └── datetime_utils.py
    ├── main.py                  ← FastAPI entry
    └── __init__.py
└── chromadb/                    ← Your data (persisted)
└── requirements.txt

Deploy for FREE (Zero Cost)

Railway → 1-click deploy
Render → Free tier
Local PC → Just run


Want More? (Next Level)

Tags & filters
PDF/Excel upload
Chat memory
Multi-user support

See my production-ready RAG chatbot:
→ Neura-Vault

License
MIT © Sanjay KM
Made with love in India • November 2025
