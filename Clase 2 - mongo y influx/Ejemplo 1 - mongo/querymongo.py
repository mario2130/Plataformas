from pymongo import MongoClient

user = "sa"
password = "vanpeh-xevtAf-7juvto"
url = f"mongodb+srv://{user}:{password}@cluster0.zq3w1va.mongodb.net/?retryWrites=true&w=majority"


mongo_client = MongoClient(url)
mongo_db = mongo_client.chucao_db
mongo_collection = mongo_db.cevezas

query = mongo_collection.find()

for doc in query:
    print(doc)

query = mongo_collection.find({"capacidad":500})

for doc in query:
    print(doc)