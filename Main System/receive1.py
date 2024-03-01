'''
UART communication on Raspberry Pi using Pyhton
http://www.electronicwings.com
'''
from asyncore import write
import serial
from time import sleep, time
import csv
import RPi.GPIO as GPIO
import datetime  

# Pins for Motor Driver Inputs 
in1 = 24
in2 = 23
en = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)
p.ChangeDutyCycle(1)

ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
while True:

    command = input("Arrived? ")
    if command == 'y':
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        print("start the timer")
        start = time()
    else:
        print("command not found")
        continue

    received_data = ser.read()              #read serial port
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)
    print (received_data)                   #print received data
    # ser.write(received_data) 

    if received_data == b'STOP':
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        print("stop the timer")
        stop = time()
        time_motor=(stop-start)
        print("Motor time: {:.2f} s".format(time_motor))

        received_data = ser.read()              #read serial port
        sleep(0.03)
        data_left = ser.inWaiting()             #check for remaining byte
        received_data += ser.read(data_left)
        CurrentDate = str(datetime.date.today())
        local_time = str(datetime.datetime.now().time())

        with open('data.csv', mode='a') as data_file:
            csv_writer = csv.writer(data_file)
            csv_writer.writerow(['Date: ' + CurrentDate + ' / Time: ' + local_time])
            csv_writer.writerow(['Temperature value: '] + [received_data])
            csv_writer.writerow([" "])

        print("run tbe motor in reverse for {:.2f} s".format(time_motor))
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        sleep(time_motor)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
