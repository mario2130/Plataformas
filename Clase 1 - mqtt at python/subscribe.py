import time
from paho.mqtt import client as mqtt_client
import json

broker = "test.mosquitto.org"
port = 1883
topic = "pucv/iot/m6/p3/g4"
temperature = list()

def connect_mqtt():
    client = mqtt_client.Client()
    client.connect(broker, port)
    return client

def subscribe(client):
    def custom_on_message(client, userdata, msg): #callback que sobre escribimos

        try:

            dataRecived = json.loads(msg.payload)
            data = dataRecived["data"]
            if(data > 0):
                temperature.append(data)
                print(f"Cantidad de valores recibidos: {len(temperature)}")
                print("Valor máximo:", max(temperature))
                print(f"Valor minimo: { min(temperature) }")
                print(f"Valor promedio: {sum(temperature)/len(temperature)}")
        except Exception as ex:
            #print(f"error: {ex}")
            i = 0

    client.subscribe(topic)
    client.on_message = custom_on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()