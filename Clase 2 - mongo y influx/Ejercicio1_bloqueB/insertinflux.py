import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS,ASYNCHRONOUS


token = "a_3AQPvFGMsWp7KZ_1JXJUe6TVVilYXTn5Pl7BRsZR73_KlfF87YLvIQUpXUoNtgcmMCjzgmeAHjmwYnWoNLLA=="
org = "mario.villanueva.gutierrez@gmail.com"
url = "https://us-east-1-1.aws.cloud2.influxdata.com"

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="chucao_db"
write_api = client.write_api(write_options=SYNCHRONOUS)

for value in range(5):
  point = (
    Point("sensor1")
    .field("temperatura", 23.56+value) #información clave
    .tag("paralelo", "3")        #información de contexto, que ayude a entender la medida    
  )
  write_api.write(bucket=bucket, org="mario.villanueva.gutierrez@gmail.com", record=point)
  time.sleep(2) # separate points by 1 second



