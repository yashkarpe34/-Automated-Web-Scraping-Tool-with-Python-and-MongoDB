from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://testy:yash9213@cluster0.bouihwi.mongodb.net/")

db = client.scrapy

posts = db.test_collection
doc = post = {
    "author": "yash",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}

post_id = posts.insert_one(post).inserted_id
print(post_id)