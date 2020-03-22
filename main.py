# -*- coding: utf-8 -*-
import os
import cv2
import time
import math
import sys
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from googletrans import Translator
translator = Translator()

import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

# Add your Computer Vision subscription key to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
   
analyze_url = endpoint + "vision/v2.1/analyze"
cap = cv2.VideoCapture("C:\\Users\\Franco\\Documents\\videosN\\2xdia.mp4") 
currentframe = 30

imagesFolder = "C:/Users/Franco/Documents/framesN"

frameRate = cap.get(5) #frame rate
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename = imagesFolder + "/image_" +  str(int(frameId)) + ".jpg"
        cv2.imwrite(filename, frame)
cap.release()
print("Done!")
cv2.destroyAllWindows() 

os.chdir(os.path.join('C:','\\Users','Franco','Documents','framesN'))
john = os.listdir(os.getcwd())

for files in john:
    
    os.chdir(os.path.join('C:','\\Users','Franco','Documents','framesN'))

    image_path = "C:/Users/Franco/Documents/framesN/"+files
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    
    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    #print(analysis)
    try:
        image_caption = analysis["description"]["captions"][0]["text"].capitalize()
        image_conf =str(analysis["description"]["captions"][0]["confidence"])
        juan =translator.translate(image_caption,src ="en", dest="es")
        
    except:
        print("base")
    jorge = juan.text
    os.chdir(os.path.join('C:','\\Users','Franco','Documents','imagenatexto'))
    archivoFile =  open('textito.txt','a')
    archivoFile.write(jorge+" "+image_conf+" "+files+"\n")
    archivoFile.close()
    archiveFile = open('liltext.txt','a')
    archiveFile.write(image_caption+" "+image_conf+" "+files+"\n")
    archiveFile.close()
    #os.remove(files)

    







