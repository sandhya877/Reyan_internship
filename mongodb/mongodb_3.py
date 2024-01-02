from fastapi import FastAPI
import pymongo
from pymongo import MongoClient 

app=FastAPI()
client=pymongo.MongoClient("mongodb+srv://sandhya:Mongodb678@cluster0.4l1eksy.mongodb.net/")

#db creation
db = client["mydatabase"]
collection = db["mycollection"]
data = {"name": "John", "age": 30}
result = collection.insert_one(data)
collection = db["mycollection"]
query = {"name": "John"}
john = collection.find_one(query)
print(john)
# reading
cursor = collection.find()
for document in cursor:
    print(document)

# db updation
collection = db["mycollection"]
query = {"name": "John"}
new_values = {"$set": {"age": 31}}
collection.update_one(query, new_values)
age = collection.find_one(query)
print(age)
#deletion
collection = db["mycollection"]
query = {"name": "John"}
collection.delete_one(query)

client.close()
