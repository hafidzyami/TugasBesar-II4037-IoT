from thingsboard_api_tools import TbApi
import time
import json
from datetime import datetime
import requests
import paho.mqtt.client as mqtt

# MQTT
broker_address = "broker.mqtt-dashboard.com"
port = 1883
client = mqtt.Client("Publisher")
client.connect(broker_address, port)
topic = "hafidzganteng/durasiservo"

# ThingsBoard
mothership_url = "http://34.101.235.1:8080"
thingsboard_username = "kel1@thingsboard.org"
thingsboard_password = "kelompok1"
tbapi = TbApi(mothership_url, thingsboard_username, thingsboard_password)
device = tbapi.get_device_by_id("98047070-7d1f-11ee-a02e-a72213eb9bb7")

# /POST ML
url = 'http://iotghaylan.byhzesbugybnbnck.southeastasia.azurecontainer.io/ml?'
headers = {'Content-Type': 'application/json'}

def mapping(x, in_min,  in_max,  out_min,  out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

irrigation = 0

while True:
    avgHumidityPercentage = (tbapi.get_telemetry(device, "Humidity",startTime=int(time.time() * 1000)-60*1000, agg="AVG"))['Humidity'][0]['value']
    print("avgHumidity : " + avgHumidityPercentage[:5] + " %")
    avgHumidity = mapping(float(avgHumidityPercentage), 0, 100, 0, 4096)
    # print("avgHumidity(analog) : ", avgHumidity)
    
    if(avgHumidity < 2048): # < 50%
        irrigation = 1
        
    with open('output.json', 'r') as file:
        data = json.load(file)
        i = 0
        while(datetime.today().strftime('%Y%m%d%H%M%S') > data['timerange'][i]['$']['datetime']):
            i += 1
        weather_code = data['timerange'][i-1]['value'][0]['_']
    
    body = {"moisture": int(avgHumidity), "irrigation": irrigation, "weather_code": int(weather_code)}
    jsondata = json.dumps(body)
    response = requests.post(url, data=jsondata, headers=headers)
    if response.status_code == 200:
        print(response.text)
        if(response.text == "[0]" or response.text == "0"):
            duration = "0"
        else:
            duration = ""
            j = 0
            while((response.text)[j] != '.'):
                duration += response.text[j]
                j += 1
        client.publish(topic, duration)
        print("Waktu yang diperlukan untuk membuka servo : " + duration + " detik, karena kode cuaca : " + weather_code)
    else:
        # Handle any errors or other status codes as needed
        print(f"Request failed with status code: {response.status_code}")
    
    # Ulangi kode setiap 6 jam sekali
    time.sleep(3600*6)