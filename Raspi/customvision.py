import requests
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import paho.mqtt.client as mqtt
import time

# URL of the image you want to download
image_url = "http://172.20.10.5/capture"

# Define the local file path where you want to save the image
local_file_path = "d" + datetime.today().strftime('%Y%m%d%H%M%S') + ".jpg"
flag = False

# Azure Custom Vision
endpoint = "https://hafidzganteng-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/4dc628bf-eb73-418f-874f-2dab9acfd873/detect/iterations/Iteration2/image"
headers = {
    "Prediction-Key": "ebd3bbd9553340939db2f70491da2cbb",
    "Content-Type": "application/octet-stream",
}
predictImageName = ""

# Azure Blob
connection_string = "DefaultEndpointsProtocol=https;AccountName=tpkiot;AccountKey=jzWgteV/05tVaUWG9BKprYJPjM5tpJn2Vmvp/jPHiJqcLskQ7bmFrffD/aTgbJpQKEe06V0aNTkt+AStjlKpBA==;EndpointSuffix=core.windows.net"
container_name = "esp32cam"

# MQTT
broker_address = "broker.mqtt-dashboard.com"
port = 1883
client = mqtt.Client("Publisher")
client.connect(broker_address, port)
topic = "hafidzganteng/detectpest"

while True:
    try:
        # Send an HTTP GET request to the image URL
        response = requests.get(image_url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the local file for binary write
            with open(local_file_path, 'wb') as file:
                # Write the content of the response to the local file
                file.write(response.content)
            print(f"Image saved as {local_file_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        
    image_data = open(local_file_path, "rb").read()
    response = requests.post(endpoint, headers=headers, data=image_data)

    if response.status_code == 200:
        predictions = response.json()
        
        image = Image.open(local_file_path)
        draw = ImageDraw.Draw(image)
        # Process and extract prediction results from 'predictions' JSON
        for prediction in predictions['predictions']:
            tag = prediction['tagName']
            probability = prediction['probability']
            bbox = prediction['boundingBox']
            
            if prediction['probability'] >= 0.6:
            # Convert normalized bounding box coordinates to pixel coordinates
                x, y, w, h = map(float, [bbox['left'], bbox['top'], bbox['width'], bbox['height']])
                x, y, w, h = int(x * image.width), int(y * image.height), int(w * image.width), int(h * image.height)

                # Draw bounding box and label
                draw.rectangle([x, y, x + w, y + h], outline=(255, 0, 0), width=2)
                font = ImageFont.load_default()
                draw.text((x, y - 12), f"{tag}: {probability:.2f}", fill=(255, 0, 0), font=font)
                if prediction['tagName'] == "WBC":
                    flag = True
                
            if flag:
                predictImageName = datetime.today().strftime('%Y%m%d%H%M%S') + ".jpg"
                image.save(predictImageName)
                client.publish(topic, 'y')
            else:
                predictImageName = 'n' + datetime.today().strftime('%Y%m%d%H%M%S') + ".jpg"
                image.save(predictImageName)    
        
    else:
        print("Prediction request failed with status code:", response.status_code)


    # Replace these variables with your own Azure Storage account details
    blob_name = predictImageName
    local_file_path = predictImageName

    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get or create a container
    container_client = blob_service_client.get_container_client(container_name)

    # Get a blob client
    blob_client = container_client.get_blob_client(blob_name)

    # Upload the local image to the blob
    with open(local_file_path, "rb") as data:
        blob_client.upload_blob(data)
    print(f"Image {blob_name} uploaded to {container_name} container.")
    
    sleep(60)