from fastapi import APIRouter

note_route = APIRouter()

@note_route.get("/")
async def user():
    return {"ping"}