from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel

from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Connect to MongoDB
client = AsyncIOMotorClient("localhost", 27017)
db = client["my_database"]
collection = db["my_collection"]

# Define a Pydantic schema for the MongoDB documents
class User(BaseModel):
    name: str
    age: int

# GET /users
@app.get("/users")
async def get_all_users():
    users = await collection.find().to_list(1000)
    return users

# GET /users/{id}
@app.get("/users/{id}")
async def get_user(id: str):
    user = await collection.find_one({"_id": id})
    return user

# POST /users
@app.post("/users")
async def create_user(user: User = Body(...)):
    new_user = await collection.insert_one(user.dict())
    return new_user

# PUT /users/{id}
@app.put("/users/{id}")
async def update_user(id: str, user: User = Body(...)):
    await collection.update_one({"_id": id}, {"$set": user.dict()})
    return user

# DELETE /users/{id}
@app.delete("/users/{id}")
async def delete_user(id: str):
    await collection.delete_one({"_id": id})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)