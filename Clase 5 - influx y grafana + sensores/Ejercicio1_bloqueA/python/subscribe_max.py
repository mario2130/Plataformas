import time
from paho.mqtt import client as mqtt_client
import json
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS,ASYNCHRONOUS

broker = "test.mosquitto.org"
port = 1883
##todos los sensores, todas las metricas (tem y hum)
topic = "pucv/iot/m6/p3/g4/devices/sensormevg/+/max"
temperature = list()
token = "a_3AQPvFGMsWp7KZ_1JXJUe6TVVilYXTn5Pl7BRsZR73_KlfF87YLvIQUpXUoNtgcmMCjzgmeAHjmwYnWoNLLA=="
org = "mario.villanueva.gutierrez@gmail.com"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="temperature_db"
write_api = client.write_api(write_options=SYNCHRONOUS)



def on_message(client, userdata, msg): #callback que sobre escribimos
    try:
        dataRecived = json.loads(msg.payload)
        print(dataRecived) 

        temperature_value = dataRecived["value"] 
        print(temperature_value)
        
            
        # point = (
        #     Point(sensor_id)
        #     .field("temperatura", temperature_value)    #información clave
        #     .tag("type", type_tag)                      #información de contexto, que ayude a entender la medida    
        # )
        # write_api.write(bucket=bucket, org="mario.villanueva.gutierrez@gmail.com", record=point)


    except Exception as ex: 
        i = 0

    

def run():
    client = mqtt_client.Client()
    client.connect(broker, port)
    client.subscribe(topic)
    client.on_message = on_message
    client.loop_forever()

if __name__ == '__main__':
    run()