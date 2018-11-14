#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests, time, os
from pathlib import Path
from time import sleep
import webbrowser


import cv2
import numpy as np

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


    UI = input("f/o: ")

    if UI == "f":
        cap = cv2.VideoCapture(0)

        # Capture frame-by-frame
        ret, frame = cap.read()

        # do what you want with frame
        #  and then save to file
        cv2.imwrite('/home/pi/Desktop/Bot/venv/Picture/image.png', frame)

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    ########################################################################################################

        imagePath = Path("/home/pi/Desktop/Bot/venv/Picture/image.png")

        #setting variables
        url= "http://localhost:1880/ORBface"

        file ={'image':open(str(imagePath),'rb')}

        #sending a request to node red
        r = requests.post(url, files=file)
        print(r.text)

##############################################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
##############################################################################################################

    else:

        cap = cv2.VideoCapture(0)

        # Capture frame-by-frame
        ret, frame = cap.read()

        # do what you want with frame
        #  and then save to file
        cv2.imwrite('/home/pi/Desktop/Bot/venv/Picture/image.png', frame)

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    ########################################################################################################

        imagePath = Path("/home/pi/Desktop/Bot/venv/Picture/image.png")

        #setting variables
        url= "http://localhost:1880/ORBobject"

        file ={'image':open(str(imagePath),'rb')}

        #sending a request to node red
        r = requests.post(url, files=file)
        print(r.text)
