from pymongo import MongoClient

user = "sa"
password = "vanpeh-xevtAf-7juvto"
url = f"mongodb+srv://{user}:{password}@cluster0.zq3w1va.mongodb.net/?retryWrites=true&w=majority"


mongo_client = MongoClient(url)
mongo_db = mongo_client.chucao_db
mongo_collection = mongo_db.cevezas

doc = {
    "marca": "corona",
    "formato": "botella-1-litro",
    "color": "rubia",
    "amargor": 2.3,
    "calidad": 0.1,
    "capacidad": 500
}

mongo_collection.insert_one(doc)
print (f"{doc}") 






