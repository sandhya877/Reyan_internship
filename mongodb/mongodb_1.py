from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb+srv://sandhya:Mongodb678@cluster0.4l1eksy.mongodb.net/")
db = client["mydatabase"]
collection = db["mycollection"]

# MongoDB Document Model
class Item(BaseModel):
    name: str
    age: int


# Create operation
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    data = {"name": item.name, "age": item.age}
    result = collection.insert_one(data)
    created_item = collection.find_one({"_id": result.inserted_id})
    return Item(**created_item)

# Read operation (get item by ID)
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    item = collection.find_one({"_id": ObjectId(item_id)})
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**item)

# Update operation (update item by ID)
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, updated_item: Item):
    query = {"_id": ObjectId(item_id)}
    new_values = {"$set": {"name": updated_item.name, "age": updated_item.age}}
    result = collection.update_one(query, new_values)
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_item_from_db = collection.find_one(query)
    return Item(**updated_item_from_db)

# Delete operation (delete item by ID)
@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    query = {"_id": ObjectId(item_id)}
    result = collection.delete_one(query)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
