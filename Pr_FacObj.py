#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests, time, os
from pathlib import Path
import RPi.GPIO as GPIO
from time import sleep
import webbrowser
import subprocess
from subprocess import Popen, PIPE

import cv2
import numpy as np

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#----------------------------DROPBOX-----------------------------------

def fileupload():


    #The directory to sync
    syncdir="/home/pi/Desktop/Bot/venv/Picture"
    #Path to the Dropbox-uploaded shell script
    uploader = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh"

    #If 1 then files will be uploaded. Set to 0 for testing
    upload = 1
    #If 1 then don't check to see if the file already exists just upload it, if 0 don't upload if already exists
    overwrite = 0
    #If 1 then crawl sub directories for files to upload
    recursive = 0
    #Delete local file on successfull upload
    deleteLocal = 1

    #Uploads a single file
    def upload_file(localPath, remotePath):
        p = Popen([uploader, "upload", localPath, remotePath], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output = p.communicate()[0].decode("utf-8").strip()
        if output.startswith("> Uploading") and output.endswith("DONE"):
            return 1
        else:
            return 0

        
    #Uploads files in a directory
    def upload_files(path, level):
        fullpath = os.path.join(syncdir,path)
        print_output("Syncing " + fullpath,level)
        if not os.path.exists(fullpath):
            print_output("Path not found: " + path, level)
        else:

            #Get a list of file/dir in the path
            filesAndDirs = os.listdir(fullpath)

            #Group files and directories
            
            files = list()
            dirs = list()

            for file in filesAndDirs:
                filepath = os.path.join(fullpath,file)
                if os.path.isfile(filepath):
                    files.append(file)       
                if os.path.isdir(filepath):
                    dirs.append(file)

            print_output(str(len(files)) + " Files, " + str(len(dirs)) + " Directories",level)

            #If the path contains files and we don't want to override get a list of files in dropbox
            if len(files) > 0 and overwrite == 0:
                dfiles = list_files(path)

            #Loop through the files to check to upload
            for f in files:                                 
                print_output("Found File: " + f,level)   
                if upload == 1 and (overwrite == 1 or not f in dfiles):
                    fullFilePath = os.path.join(fullpath,f)
                    relativeFilePath = os.path.join(path,f)  
                    print_output("Uploading File: " + f,level+1)   
                    if upload_file(fullFilePath, relativeFilePath) == 1:
                        print_output("Uploaded File: " + f,level + 1)
                        if deleteLocal == 1:
                            print_output("Deleting File: " + f,level + 1)
                            os.remove(fullFilePath)                        
                    else:
                        print_output("Error Uploading File: " + f,level + 1)
                        
            #If recursive loop through the directories   
            if recursive == 1:
                for d in dirs:
                    print_output("Found Directory: " + d, level)
                    relativePath = os.path.join(path,d)
                    upload_files(relativePath, level + 1)
                

                    

                    
    #Start
    upload_files("",1)
    
#------------------------------------Dropbox---------------------------------------    
    
while True:
    try:
        r = requests.get("http://localhost:1880")
        status = r.status_code

        if status == 200:
            print("-"*30 + "\nAll Functions Ready!\n" + "-"*30)

    except requests.ConnectionError:
        continue

    break

os.system("omxplayer -o local /home/pi/Downloads/beep.wav")



while True:

    if (GPIO.input(13) == False):
        print ("Pin 13 is true")

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
        
        fileupload()
        
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
        
        fileupload()
