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


def publish(client):
    counter = 0
    while True:
        time.sleep(3)

        data = {
            "counter": counter,
            "type" : "contador",
            "paralelo": "3.0",
            "otra": "kkave",
            "temperatura": 22.5 + counter
        }

        #msg = f"contador: {counter}"
        msg = json.dumps(data)
        client.publish(topic, msg)
        counter += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()