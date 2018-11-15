#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests, time, os
from pathlib import Path
import RPi.GPIO as GPIO
from time import sleep
import webbrowser


import cv2
import numpy as np

GPIO.setmode(GPIO.BCM)

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)


while True:
    try:
        r = requests.get("http://localhost:1880")
        status = r.status_code

        if status == 200:
            webbrowser.open("http://localhost:1880", new=1, autoraise=False)

    except requests.ConnectionError:
        continue

    break

sleep(10)

os.system("chromium-browser file:///home/pi/Desktop/Bot/venv/bin/cutie.html")
time.sleep(5)
os.system("xdotool key F11")


os.system("omxplayer /home/pi/Downloads/beep.wav")

while True:

    if (GPIO.input(10) == False):
        print ("Pin 10 is true")

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite('/home/pi/Desktop/Bot/venv/Picture/image.png', frame)
        cap.release()
        cv2.destroyAllWindows()

        imagePath = Path("/home/pi/Desktop/Bot/venv/Picture/image.png")

        #setting variables
        url= "http://localhost:1880/ORBface"

        file ={'image':open(str(imagePath),'rb')}

        #sending a request to node red
        r = requests.post(url, files=file)
        print(r.text)
        
    elif(GPIO.input(21) == False):
        print ("Pin 21 is true")

        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite('/home/pi/Desktop/Bot/venv/Picture/image.png', frame)
        cap.release()
        cv2.destroyAllWindows()

        imagePath = Path("/home/pi/Desktop/Bot/venv/Picture/image.png")

        #setting variables
        url= "http://localhost:1880/ORBobject"

        file ={'image':open(str(imagePath),'rb')}

        #sending a request to node red
        r = requests.post(url, files=file)
        print(r.text)