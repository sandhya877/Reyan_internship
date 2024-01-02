from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId  # Import ObjectId from bson module
from fastapi.responses import JSONResponse

app = FastAPI()

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27023"
MONGO_DB = "simpleghar"

# Define MongoDB client and database
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]

class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

@app.post("/api/users", response_model=dict)
async def create_user(user: UserCreate):
    try:
        # Insert user into the existing MongoDB collection (moderator)
        result = await db.moderator.insert_one(user.dict())
        inserted_user = await db.moderator.find_one({"_id": result.inserted_id})

        # Convert ObjectId to string
        inserted_user['_id'] = str(inserted_user['_id'])

        return {"message": "User added successfully", "user": inserted_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# API endpoint to get a list of users
@app.get("/api/users", response_model=list[UserResponse])
async def get_users():
    try:
        users = await db.moderator.find().to_list(length=None)
        users = [
            {"id": str(user['_id']), "username": user['username'], "email": user['email']}
            for user in users
        ]

        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

collection = db["scraping_data"]

@app.get("/get_product_details/")
async def get_product_details(image_url: str = Query(..., title="Image URL")):
    result = await collection.find_one({"top_selling_products.images": image_url})

    if result:
        # Extract product details
        product_name = result.get("top_selling_products")[0].get("name")
        price = result.get("top_selling_products")[0].get("price")
        # Add more fields as needed

        # Convert ObjectId to string
        result['_id'] = str(result['_id'])

        # Return the product details
        response = {
            "product_name": product_name,
            "price": price,
            "_id": result['_id'],  # Convert ObjectId to string
            # Add more fields as needed
        }
        return response
    else:
        raise HTTPException(status_code=404, detail="Product not found")

# FastAPI route to retrieve top selling products
@app.get("/get_top_selling_products")
async def get_top_selling_products():
    # Query MongoDB collection to find documents with top selling products
    results = collection.find({"top_selling_products": {"$exists": True}})

    # Extract and format the details of top selling products from the documents
    top_selling_products = []
    
    async for result in results:
        top_selling_product = result['top_selling_products'][0]
        product_details = {
            "ASIN": top_selling_product['asin'],
            "Rank": top_selling_product['rank'],
            "Rating": f"{top_selling_product['rating']['rating']} ({top_selling_product['rating']['rating_count']} ratings)",
            "Name": top_selling_product['name'],
            "Price": f"{top_selling_product['price']['price']} {top_selling_product['price']['price_unit']}",
            "_id": str(result['_id'])  # Convert ObjectId to string
        }
        top_selling_products.append(product_details)

    # Return the list of top selling products as JSON response
    return {"top_selling_products": top_selling_products}

@app.get("/get_all_records")
async def get_all_records():
    try:
        # Retrieve all documents from the collection
        cursor = collection.find({})
        all_records = [document async for document in cursor]  # Use 'async for' here

        # Convert ObjectId to string in each document
        for record in all_records:
            record['_id'] = str(record['_id'])

        return JSONResponse(content={"status": "success", "data": all_records})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})

# Run FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
