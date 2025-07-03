from pydantic import BaseModel
from db.user import User
from fastapi import FastAPI


class RoleCreate(BaseModel):
    name: str



app = FastAPI()

@app.post("/role/")
async def create_item(role: RoleCreate):
    return role