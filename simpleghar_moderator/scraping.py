from fastapi import FastAPI, Depends ,HTTPException
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.responses import JSONResponse
from urllib.parse import quote
app = FastAPI()

# Connect to your MongoDB instance
client = AsyncIOMotorClient('mongodb://localhost:27023')
database = client['simpleghar']
collection = database['scraping']


async def get_mongo_db():
    db = client['simpleghar']
    yield db
    client.close()

@app.get("/get_all_image_urls")
async def get_all_image_urls(db: database = Depends(get_mongo_db)):
    try:
        # Retrieve all documents in the collection
        cursor = collection.find()

        # Use to_list to convert the cursor to a list
        documents = await cursor.to_list(length=1000)

        # Extract all image URLs from the documents
        all_image_urls = []
        for document in documents:
            for product in document.get("top_selling_products", []):
                all_image_urls.extend(product.get("images", []))

        return JSONResponse(content={"all_image_urls": all_image_urls})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)



@app.get("/get_product_by_image_url")
async def get_product_by_image_url( db: database = Depends(get_mongo_db)):
    try:
        image_url="https://images-eu.ssl-images-amazon.com/images/I/71hP1JEHDFL._AC_UL300_SR300,200_.jpg"
        cursor = collection.find()
        documents = await cursor.to_list(length=1000)
        for document in documents:
            for product in document.get("top_selling_products", []):
                if image_url in product.get("images", []):
                    return product
        
        
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

 