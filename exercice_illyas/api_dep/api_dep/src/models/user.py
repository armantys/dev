from pydantic import BaseModel
from db.user import User
from fastapi import FastAPI


class CreateUser(BaseModel):

    username: str
    password: str



app = FastAPI()

@app.post("/user/")
async def create_item(user: CreateUser):
    return user
