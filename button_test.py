import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:

   if (GPIO.input(10) == False):
      print ("Pin 10 is true")
      # do stuff based on pin 10 here
   elif(GPIO.input(21) == False):
      print ("Pin 21 is true")
      # do stuff based on pin 21 here
