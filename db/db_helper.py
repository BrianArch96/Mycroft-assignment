import pymongo
from pymongo import MongoClient

url = "mongodb://Archie96:hannah10@mycroft-assignment-shard-00-00-1rt5b.mongodb.net:27017,mycroft-assignment-shard-00-01-1rt5b.mongodb.net:27017,mycroft-assignment-shard-00-02-1rt5b.mongodb.net:27017/test?ssl=true&replicaSet=Mycroft-Assignment-shard-0&authSource=admin&retryWrites=true"
client = MongoClient(url)
client.server_info()
db = client['test']
my_collection = db['test']
post = {"author": "Brian",
        "test": "testing this stuff"
        }
posts = db.tester
post_id = posts.insert_one(post).inserted_id
