#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <PubSubClient.h> 
#include <DallasTemperature.h>
#include <OneWire.h>

#define temperatureSensor D2

char* ssid = "IoTNetWork";
char* password = "desarrollo123";
OneWire oneWire(temperatureSensor);
DallasTemperature sensors(&oneWire);

const char* mqttServer = "test.mosquitto.org";
int port = 1883;
const char* subscribeTopic = "pucv/iot/m6/p3/g4";

WiFiClient espClient;
PubSubClient client(espClient);
char clientId[50];
DynamicJsonDocument doc(1024);
char* data = "";


void setup(){
    Serial.begin(115200);
    pinMode(temperatureSensor, INPUT);
    delay(500);
    
    Serial.print("Conectando a WiFi ");
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("conectado");

    //***** Obtener direccion IP asignada *******
    IPAddress ip;
    ip = WiFi.localIP();
    Serial.print("Direccion IP: ");
    Serial.println(ip);

    //***** Configurando MQTT Client ************
    client.setServer(mqttServer, port); 

}

void loop(){
    delay(1000);
    sensors.requestTemperatures();
    float temperatureValue = sensors.getTempCByIndex(0);
  
    Serial.println(temperatureValue);
    if (client.connected())
    {
      doc["data"] = temperatureValue;
      String serializedJSON;
      serializeJson(doc, serializedJSON);
      client.publish(subscribeTopic,serializedJSON.c_str()); 
      Serial.println("publish succefully");
    }
    else
    {
      mqttReconnect();      
    }
    client.loop();
}

 

void mqttReconnect(){
    while (!client.connected()){
        Serial.print("Intentando conectar al broker MQTT con cliente ");
        long r = random(1000);
        sprintf(clientId, "clientId-%ld", r);
        if (client.connect(clientId)){
            Serial.print(clientId);
            Serial.println(".......conectado");
            client.subscribe(subscribeTopic);
        }
        else{
            Serial.print("falló, rc=");
            Serial.print(client.state());
            Serial.println(".....Reintentando en 5 segundos");
            delay(5000);
        }
    }
}
