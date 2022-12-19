from flask_restful import Resource
from flask import request

_list = []
_element = {
    "Id": "0",
    "SensorType" : "humedity",
    "SensorValue" : 23.5
}


class SensorList(Resource):

    def get(self):
        return _list
    def post(self):
        global indice
        id = indice
        request_body = request.json
        indice += 1
        request_body["Id"] = indice
        print(request_body)
        _list.append(request_body)
       
        return request_body, 201