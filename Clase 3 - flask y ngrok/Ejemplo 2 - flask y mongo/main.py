from json import dumps
from flask import Flask, request, Response
from flask_restful import Api, Resource
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from http import *

user = "sa"
password = "vanpeh-xevtAf-7juvto"
url = f"mongodb+srv://{user}:{password}@cluster0.zq3w1va.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__)
api = Api(app)


mongo_client = MongoClient(url)
mongo_db = mongo_client.sensors_db


class SensorsList(Resource):
    mongo_collection = mongo_db.sensor
    def get(self):  
        result = list()     
        query = self.mongo_collection.find() 
        for doc in query:
            result.append(doc)
        return Response(response=dumps(result, default=str),
                    status=200,
                    mimetype='application/json')

    def post(self): 
        request_body = request.get_json()        
        print(request_body)
        self.mongo_collection.insert_one(request_body)
        return '', 201

class Sensor(Resource):
    mongo_collection = mongo_db.sensor
   
    def get(self, id): 
        data = self.mongo_collection.find_one({'_id': ObjectId(id)})       
        return Response(response=dumps(data, default=str),
                    status=200,
                    mimetype='application/json')
 
    def delete(self, id): 
        self.mongo_collection.delete_one({'_id': ObjectId(id)})       
        return Response(response=dumps(data, default=str),
                    status=200,
                    mimetype='application/json')

api.add_resource(SensorsList, "/sensors")
api.add_resource(Sensor, "/sensors/<id>")

if __name__ == '__main__':
    app.run(debug=True)