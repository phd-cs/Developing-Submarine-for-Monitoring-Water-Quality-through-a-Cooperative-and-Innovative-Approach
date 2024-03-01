#Libraries
import RPi.GPIO as GPIO
import time
import os
from time import sleep
import serial
os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")
temp_sensor = '/sys/bus/w1/devices/28-000006535e41/w1_slave'

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
ser.reset_input_buffer()

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO =24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def read_temp_raw():

   f = open(temp_sensor, 'r')
   lines = f.readlines()
   f.close()
   return lines

def read_temp():

  lines = read_temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    sleep(0.2)
  lines = read_temp_raw()
#   print(lines)
  temp_result = lines[1].find('t=')
#   print(temp_result)
  if temp_result != -1:
    temp_string = lines[1].strip()[temp_result + 2:]
    # print(temp_string)
    # Temperature in Celcius
    temp = float(temp_string) / 1000.0
    # Temperature in Fahrenheit
    #temp = ((float(temp_string) / 1000.0) * (9.0 / 5.0)) + 32.0
    return temp

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

    
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            sleep(1)
            if dist < 10:
                sleep(1)
                data = read_temp()
                data_b = bytes(str(data), 'utf-8')
                print(data)
                ser.write(data_b)
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
