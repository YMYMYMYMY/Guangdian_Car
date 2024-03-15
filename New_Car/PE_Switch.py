import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

PE_Switch = 7

GPIO.setup(PE_Switch, GPIO.IN)
PE_S = GPIO.input(PE_Switch)

i = 1
while(i):
    PE_S = GPIO.input(PE_Switch)
    if PE_S == 0:
        print("dididididi")
        i = 0
    if PE_S == 1:
        i = 1
