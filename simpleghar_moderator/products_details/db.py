from pymongo import MongoClient
from bson.objectid import ObjectId
import json
from bson import json_util
from bson import ObjectId


# Placeholder for MongoDB connection (should use environment variables or config files)
client = MongoClient('mongodb://localhost:27023/')
db = client['articles']

# # Function to get the category collection
# def get_category_collection():
#     return db['new_categories']

# def get_products_collection():
#     return db['products']



def insert_data(collection_name, data):
    collection = db[collection_name]
    if isinstance(data, dict):
        insert_result = collection.insert_one(data)
        inserted_id = str(insert_result.inserted_id)
        return inserted_id # Return the inserted document
    elif isinstance(data, list):
        insert_result = collection.insert_many(data)
        inserted_ids = [str(_id) for _id in insert_result.inserted_ids]
        return inserted_ids # Return list of inserted documents


def get_data(collection_name):
    collection = db[collection_name]
    data = list(collection.find())
    for item in data:
        item["_id"] = str(item["_id"])  # Convert ObjectId to string
    return data

def get_data_by_id(collection_name, data_id):
    collection = db[collection_name]
    data = collection.find_one({"_id": ObjectId(data_id)})
    if data:
        data["_id"] = str(data["_id"])  # Convert ObjectId to string
    return data

def update_data(collection_name, data_id, new_data):
    collection = db[collection_name]
    update_result = collection.update_one({"_id": ObjectId(data_id)}, {"$set": new_data})
    if update_result.modified_count > 0:
        updated_data = collection.find_one({"_id": ObjectId(data_id)})
        if updated_data:
            updated_data["_id"] = str(updated_data["_id"])  # Convert ObjectId to string
        return updated_data
    return None  # Return None if no document was updated

def delete_data(collection_name, data_id):
    collection = db[collection_name]
    deleted_data = collection.find_one({"_id": ObjectId(data_id)})
    if deleted_data:
        deleted_data["_id"] = str(deleted_data["_id"])  # Convert ObjectId to string
    collection.delete_one({"_id": ObjectId(data_id)})
    return deleted_data


def update_moderators_by_article_id(collection, article_id):
    try:
        collection = db[collection]
        article_object_id = ObjectId(article_id)
        print(collection)
        print(article_object_id)

        # Update the moderator items where the ArticlesAssociated field contains the deleted article ID
        update_query = {"$pull": {"ArticlesAssociated": article_id}}

        # Update multiple documents in the collection
        update_result = collection.update_many({"ArticlesAssociated": article_id}, update_query)

        return update_result.modified_count if update_result else 0

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0