import RPi.GPIO as GPIO          
from time import sleep

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)
p.ChangeDutyCycle(1)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
print("forward")
sleep(3)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.HIGH)
print("backward")
sleep(3)

print("stop")
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)