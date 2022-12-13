import time
from paho.mqtt import client as mqtt_client
import json

broker = "test.mosquitto.org"
port = 1883
topic = "pucv/iot/sensores"


def connect_mqtt():
    client = mqtt_client.Client()
    client.connect(broker, port)
    return client

def subscribe(client):
    def custom_on_message(client, userdata, msg): #callback que sobre escribimos
        print(msg.payload)



    client.subscribe(topic)
    client.on_message = custom_on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()