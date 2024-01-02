from fastapi import FastAPI ,Path
import pymongo
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId from bson

app = FastAPI()

# Initialize the MongoDB client and select the database and collection
client = pymongo.MongoClient("mongodb+srv://sandhya:Mongodb678@cluster0.4l1eksy.mongodb.net/")
db = client["mydatabase"]
collection = db["mycollection"]
from fastapi import FastAPI, HTTPException, Body
import pymongo
from pymongo import MongoClient

app = FastAPI()

# Initialize the MongoDB client and select the database and collection
client = pymongo.MongoClient("mongodb+srv://sandhya:Mongodb678@cluster0.4l1eksy.mongodb.net/")
db = client["mydatabase"]
collection = db["mycollection"]

@app.post("/insert_user")
async def insert_user(name: str = Body(..., title="Name of the user"), age: int = Body(..., title="Age of the user")):
    user_data = {"name": name, "age": age}
    result = collection.insert_one(user_data)

    if result.inserted_id:
        return {"message": "User data inserted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to insert user data")
    


@app.get("/get_data/{name}")
async def get_data(name: str):
    query = {"name": name}
    data = collection.find_one(query)

    if data:
        data["_id"] = str(data["_id"])
        return data
    else:
        return {"message": "Data not found"}

@app.get("/get_all_data")
async def get_all_data():
    cursor = collection.find()
    data_list = []

    for document in cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    if data_list:
        return data_list
    else:
        return {"message": "No data found"}
    
@app.put("/update_user_by_name/{name}")
async def update_user_by_name(
    name: str = Path(..., title="Name of the user to update"),
    update_data: dict = Body(..., title="New user data to update")
):
    # Check if a document with the provided name exists
    user = collection.find_one({"name": name})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with name '{name}' not found")

    # Perform the update using update_one
    result = collection.update_one({"name": name}, {"$set": update_data})

    if result.modified_count > 0:
        return {"message": f"User '{name}' updated successfully"}
    else:
        raise HTTPException(status_code=500, detail=f"Failed to update user '{name}'")
    
@app.delete("/delete_user/{name}")
async def delete_user(name: str = Path(..., title="Name of the user to delete")):
    user = collection.find_one({"name": name})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with name '{name}' not found")
    result = collection.delete_one({"name": name})

    if result.deleted_count > 0:
        return {"message": f"User '{name}' deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail=f"Failed to delete user '{name}'")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
