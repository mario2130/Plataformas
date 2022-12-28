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
 

const char* mqttServer = "industrial.api.ubidots.com";
int port = 1883;
WiFiClient espClient;
PubSubClient client(espClient);
char clientId[50];


DynamicJsonDocument json(1024); 
char* topicBase = "/v1.6/devices/sensormevg";
char topicSensor[200]; 

float temperatureValue = 0;
float temperatureMax = 0;
float temperatureMin = 9999;
float temperatureAvg = 0;
float temperatureAcumulate = 0;

int sensoresCount = 0;
float humedityValue = 10;
const char* mqtt_password = "";
const char* mqtt_user = "BBFF-ff1kVAWEmxqKwWVRyayiCY72AdTPMM";

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
    delay(5000);
    sensors.requestTemperatures();
    temperatureValue = sensors.getTempCByIndex(0);
    humedityValue = 10;
    sensoresCount += 1;

    Serial.print("temperature: ");
    Serial.println(temperatureValue);
    Serial.print("humedity: ");
    Serial.println(humedityValue);
    Serial.print("sensores Count: ");
    Serial.println(sensoresCount);

    if (client.connected())
    { 
      sendTemperature();
      sendTemperatureMax();
      sendTemperatureMin();
      sendTemperatureAvg();
      sendHumedity();
      
    }
    else
    {
      mqttReconnect();      
    }
    client.loop();
}

 void sendTemperature()
 {
    char* sensorName = "/temperature"; 
    send(sensorName, temperatureValue);   
 }


void send(char* topicValue, float value)
{  
  strcpy(topicSensor,topicBase);
  strcat(topicSensor,topicValue);  
  json["value"] = value;
  json["context"] ="{\"lat\":-6.2, \"lng\":75.4}";
  String serializedJSON;
  serializeJson(json, serializedJSON);
  client.publish(topicSensor,serializedJSON.c_str());  
  Serial.print(topicSensor);
  Serial.println(" send ok");
}

void sendTemperatureMax()
{
  if(temperatureValue > temperatureMax)
  {
    temperatureMax = temperatureValue;
  }

  char* sensorName = "/temperature/max";  
  send(sensorName, temperatureMax);    
}

void sendHumedity()
{  
  char* sensorName = "/humedity"; 
  send(sensorName, humedityValue);
}

void sendTemperatureMin()
{ 
  if(temperatureValue < temperatureMin)
  {
    temperatureMin = temperatureValue;
  }

  char* sensorName = "/temperature/min";  
  send(sensorName, temperatureMin);    
}

void sendTemperatureAvg()
{ 
  temperatureAcumulate += temperatureValue;
  

  char* sensorName = "/temperature/avg";  
  send(sensorName, temperatureAcumulate/sensoresCount);    
}

void mqttReconnect(){
    while (!client.connected()){
        Serial.print("Intentando conectar al broker MQTT con cliente ");
        long r = random(1000);
        sprintf(clientId, "clientId-%ld", r);
        if (client.connect(clientId, mqtt_user, mqtt_password)){
            Serial.print(clientId);
            Serial.println(".......conectado");
            client.subscribe(topicBase);
        }
        else{
            Serial.print("falló, rc=");
            Serial.print(client.state());
            Serial.println(".....Reintentando en 5 segundos");
            delay(5000);
        }
    }
}
