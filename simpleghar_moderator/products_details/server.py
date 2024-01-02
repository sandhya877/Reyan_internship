import os
import uvicorn
from fastapi import FastAPI
# from routers.v1 import router as v1_router
# from config import settings

from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
from model import Article, Moderator, ProductURLDetails
import db as db
import constants as c
from bson.objectid import ObjectId

app = FastAPI()

# Versioned API routing
# app.include_router(v1_router.router, prefix='/v1')

"""
API 2- live products + out of stock check api (assuming they are in database) ; Payload : article title; Part key, sort key as title - get all product urls in it for each url : Check the stock details in database and return live products, out of stock count 

PAGE 2 : ADD NEW ARTICLE 
Api 2 : payload : {List of urls } Get all product data from database based on the url. Response : return product data for all urls 

"""

@app.post("/save_article")
async def save_article(article: Article):
    # Calculate number of products based on URL count
    num_products = len(article.product_urls)
    collection_name = c.article_collection_name

    # Generate published date (current date/time)
    published_date = datetime.utcnow()

    product_urls_data = [{"url": url.url, "tag": url.tag} for url in article.product_urls]
    # Create a document to save in the database
    article_data = {
        "Title": article.title,
        "ParentTag": article.parent_tag,
        "ChildTag": article.child_tag,
        "ProductUrls": product_urls_data,
        "ModeratorName": article.moderator_name,
        "NumProducts": num_products,
        "PublishedDate": published_date,
        "ModifiedDate": published_date 
    }
    print("ok1")
    # Insert the document into the database
    result = db.insert_data(collection_name, article_data)
    print(result)
    print("ok2")

    return {
        "message": f"Product data saved successfully", "result":result
    }


@app.put("/update_article/{article_id}")
async def update_article(article_id: str, article: Article):
    # Fetch the existing product from the database
    existing_article = db.get_data_by_id( c.article_collection_name ,article_id)

    # If the product does not exist, return an error
    if not existing_article:
        return {"message": "Product not found"}

    updated_product_urls = [{"url": url.url, "tag": url.tag} for url in article.product_urls]
    # Update the product details
    update_data = {
        "Title": article.title,
        "ParentTag": article.parent_tag,
        "ChildTag": article.child_tag,
        "ProductUrls": updated_product_urls,
        "ModeratorName": article.moderator_name,
        "NumProducts": len(article.product_urls),
        "ModifiedDate": datetime.utcnow()  # Update modified date
    }

    # Perform the update operation
    result = db.update_data(c.article_collection_name, article_id, update_data)

    return {"message": "Product updated successfully", "result": result}



# @app.delete("/delete_article/{article_id}")
# async def delete_article(article_id: str):
#     result = db.delete_data(c.article_collection_name, article_id)
#     if result:
#         return {"message": "Article deleted successfully", "result": result}
#     return {"message": "Article not found"}




@app.delete("/delete_article/{article_id}")
async def delete_article(article_id: str):
    result = db.delete_data(c.article_collection_name, article_id)
    if result:
        # Update associated moderators
        collection_name = c.moderator_collection_name
        print(collection_name)
        update_count = db.update_moderators_by_article_id(collection_name, article_id)
        print(update_count)
        if update_count > 0:
            return {"message": "Article deleted successfully along with associated moderators update", "result": result}
    
    return {"message": "Article not found or associated moderators not updated"}


@app.get("/get_article/{article_id}")
async def get_article(article_id: str):
    article = db.get_data_by_id(c.article_collection_name, article_id)
    if article:
        return {"message": "Article retrieved successfully", "article": article}
    return {"message": "Article not found"}


@app.get("/get_articles")
async def get_articles():
    articles = db.get_data(c.article_collection_name)
    return {"message": "Articles retrieved successfully", "articles": articles}


# MODERATOR DETAILS APIS 


@app.post("/add_moderator")
async def save_moderator(moderator: Moderator):
    collection_name = c.moderator_collection_name
    moderator_data = {
        "Name": moderator.name,
        "ArticlesAssociated": moderator.article_ids
    }
    result = db.insert_data(collection_name, moderator_data)
    return {"message": "Moderator saved successfully", "result": result}


@app.put("/update_moderator/{moderator_id}")
async def update_moderator(moderator_id: str, moderator: Moderator):
    collection_name = c.moderator_collection_name
    existing_moderator = db.get_data_by_id(collection_name, moderator_id)
    if not existing_moderator:
        return {"message": "Moderator not found"}
    
    update_data = {
        "Name": moderator.name,
        "ArticlesAssociated": moderator.article_ids
    }
    result = db.update_data(collection_name, moderator_id, update_data)
    return {"message": "Moderator updated successfully", "result": result}


@app.delete("/delete_moderator/{moderator_id}")
async def delete_moderator(moderator_id: str):
    collection_name = c.moderator_collection_name
    result = db.delete_data(collection_name, moderator_id)
    if result:
        return {"message": "Moderator deleted successfully", "result": result}
    return {"message": "Moderator not found"}


@app.get("/get_moderators")
async def get_moderators():
    collection_name = c.moderator_collection_name
    moderators = db.get_data(collection_name)
    return {"message": "Moderators retrieved successfully", "moderators": moderators}


@app.get("/get_moderator/{moderator_id}")
async def get_moderator(moderator_id: str):
    collection_name = c.moderator_collection_name
    moderator = db.get_data_by_id(collection_name, moderator_id)
    if moderator:
        article_ids = moderator.get("ArticlesAssociated", [])  # Get associated article IDs
        article_collection = c.article_collection_name
        articles = []
        for article_id in article_ids:
            try:
                article = db.get_data_by_id(article_collection, article_id)
                if article:
                    articles.append(article)
                else:
                    articles.append({"message": f"Article with ID {article_id} not found"})
            except Exception as e:
                articles.append({"message": f"Error retrieving article with ID {article_id}: {str(e)}"})
        moderator["articles"] = articles  # Add article data to the moderator object
        return {"message": "Moderator retrieved successfully", "moderator": moderator}
    return {"message": "Moderator not found"}

@app.get("/get_moderators_detailed")
async def get_moderators():
    collection_name = c.moderator_collection_name
    moderators = db.get_data(collection_name)
    for moderator in moderators:
        article_ids = moderator.get("ArticlesAssociated", [])  # Get associated article IDs
        article_collection = c.article_collection_name
        articles = []
        for article_id in article_ids:
            try:
                article = db.get_data_by_id(article_collection, article_id)
                if article:
                    articles.append(article)
                else:
                    articles.append({"message": f"Article with ID {article_id} not found"})
            except Exception as e:
                articles.append({"message": f"Error retrieving article with ID {article_id}: {str(e)}"})
        moderator["articles"] = articles  # Add article data to each moderator object
    return {"message": "Moderators retrieved successfully", "moderators": moderators}



@app.put("/associate_articles/{moderator_id}")
async def associate_articles(moderator_id: str, articles: List[str]):
    collection_name = c.moderator_collection_name
    existing_moderator = db.get_data_by_id(collection_name, moderator_id)
    if not existing_moderator:
        return {"message": "Moderator not found"}

    update_data = {
        "ArticlesAssociated": articles
    }
    result = db.update_data(collection_name, moderator_id, update_data)
    return {"message": "Articles associated successfully", "result": result}





@app.put("/update_article_urls/{article_id}")
async def update_article_urls(article_id: str, product_urls: List[ProductURLDetails]):
    # Fetch the existing article from the database
    existing_article = db.get_data_by_id(c.article_collection_name, article_id)

    # If the article does not exist, return an error
    if not existing_article:
        return {"message": "Article not found"}

    # Extract the existing product URLs from the article
    existing_urls = existing_article.get("ProductUrls", [])

    # Update the product URLs with tags provided in the payload
    updated_urls = []
    for new_url_data in product_urls:
        # Check if the URL exists in the existing URLs
        url_exists = False
        for existing_url_data in existing_urls:
            if existing_url_data["url"] == new_url_data.url:
                existing_url_data["tag"] = new_url_data.tag  # Update the tag for the existing URL
                updated_urls.append(existing_url_data)
                url_exists = True
                break

        if not url_exists:
            # If the URL is new, add it with the provided tag
            updated_urls.append({"url": new_url_data.url, "tag": new_url_data.tag})

    # Update the article data with the modified URLs
    update_data = {"ProductUrls": updated_urls, "ModifiedDate": datetime.utcnow()}

    # Perform the update operation
    result = db.update_data(c.article_collection_name, article_id, update_data)

    return {"message": "Article URLs updated successfully", "result": result}



 


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8070, reload=True)
