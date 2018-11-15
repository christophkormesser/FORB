import RPi.GPIO as gpio

gpio.setwarnings(False)
gpio.setmode(gpio.BOARD)
gpio.setup(10, gpio.IN, pull_up_down=gpio.PUD_DOWN)

while True:
    if gpio.input(10) == gpio.HIGH:
        print("Button pressed!")
