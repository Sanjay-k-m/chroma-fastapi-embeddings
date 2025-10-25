from fastapi import FastAPI
from routes import note_route



app = FastAPI(title="chroma-fastapi-embeddings",description=" ")


# routes
##############################################################



app.include_router(note_route,prefix="/note" , tags=["note"])

##############################################################
@app.get('/')
async def root():
    return {"Server is Running......."}