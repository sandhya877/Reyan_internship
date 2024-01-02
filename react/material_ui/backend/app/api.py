from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27023/')
db = client['reyan']
collection = db['amazon']

# Pydantic model for item
class Item(BaseModel):
    link: str  # Add the link field
    title: str
    img: str
    

# Function to convert ObjectId to string
def str_to_id(item):
    item["_id"] = str(item["_id"])
    return item

origins = [
    "http://localhost:3000",
    "localhost:3000"
]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Replace with the appropriate frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a new item
@app.post("/items/")
async def create_item(item: Item):
    new_item = dict(item)
    result = collection.insert_one(new_item)
    return {"message": "Item created successfully", "item_id": str(result.inserted_id)}

# Get all items
@app.get("/items/")
async def read_items():
    items = list(collection.find({}))
    return list(map(str_to_id, items))

# Get a specific item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return str_to_id(item)  # Convert ObjectId to string
    raise HTTPException(status_code=404, detail="Item not found")

# Update an item by ID
@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    updated_item = dict(item)
    result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": updated_item})
    if result.modified_count == 1:
        return {"message": "Item updated successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# Delete an item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
