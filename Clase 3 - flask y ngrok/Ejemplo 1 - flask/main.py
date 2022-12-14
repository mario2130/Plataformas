from flask import Flask
from flask_restful import Api
from Entities.Sensor import SensorList

app = Flask(__name__)
api = Api(app)



api.add_resource(SensorList,"/sensors")

if __name__ == '__main__':
    app.run(debug=True)