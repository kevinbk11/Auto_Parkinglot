import threading
import time
import RPi.GPIO as GPIO
import cv2 as cv
import find
import CutAndNet
import os
DataRoot=r"Produce\DataBase.pt"
MONITOR_PIN = 4
MONITOR_PIN1 = 5
btm = 7
cap=cv.VideoCapture(0)
GPIO.setmode(GPIO.BCM)
delay=0

def BackDoor():
    while True:
        GPIO.setup(MONITOR_PIN1, GPIO.OUT)
        GPIO.output(MONITOR_PIN1, GPIO.LOW)
        time.sleep(0.1)
 
        count = 0
        GPIO.setup(MONITOR_PIN1, GPIO.IN)
        while (GPIO.input(MONITOR_PIN1) == GPIO.LOW):
            count += 1
        if count>=600:
            BackDoorMotor.open()
            time.sleep(10)
            BackDoorMotor.close()

def FrontDoor():
    while True:
        GPIO.setup(MONITOR_PIN, GPIO.OUT)
        GPIO.output(MONITOR_PIN, GPIO.LOW)
        time.sleep(0.1)

        count = 0
        GPIO.setup(MONITOR_PIN1, GPIO.IN)
        while (GPIO.input(MONITOR_PIN1) == GPIO.LOW):
            count += 1
        if count>=600:
            while delay==999999:
                print("有人正在取車,請稍後")
                time.sleep(1)
            delay=99999
            img=cap.read()
            Find,img=find.lpr(img)
            if Find:
                fp=open(DataRoot,"r")
                x=fp.readline().split()
                fp.close()
                ans=CutAndNet.read(img)
                for w in range(8):
                    if x[w]=="None":
                        if w==0:
                            delay(10)
                        else:
                            m.run(45*w)
                        x[w]=ans
                ff=open(DataRoot,"w")
                ff.write()
                ff.close()
                fff=open(DataRoot,"a")
                for a in x:
                    ff.write(a+" ")
                FrontDoorMotor.open()
                time.sleep(10)
                FrontDoorMotor.close()
                delay=0
        sleep(delay)
    
fp=open(DataRoot,"r")
carlist=["n" for x in range(8)]
x=fp.readline().split()
r=0
for h in x:
    carlist[r]=h
    r+=1
fp.close() 
Front=threading.Thread(target=FrontDoor)
Back=threading.Thread(target=BackDoor)
Front.start()
Back.start()
GPIO.setup(btm,GPIO.IN)
while True:
    time.sleep(delay)
    if GPIO.input(btm)==GPIO.HIGH:
        while delay==99999:
            print("有人正在停車,請稍後")
            time.sleep(1)
        delay=999999
        x = input()
        w=open(DataRoot,"r")
        n=w.readline().split()
        for f in range(8):
            if n[f]==x:
                n[f]="None"
        w.close()
        ww=open(DataRoot,"w")
        ww.write("")
        ww.close()
        www=open(DataRoot,"a")
        for h in n:
            www.write(h+" ")
        delay=0


















'''x = input()
w=open(DataRoot,"r")
n=w.readline().split()
for f in range(8):
    if n[f]==x:
        n[f]="None"
w.close()
ww=open(DataRoot,"w")
ww.write("")
ww.close()
www=open(DataRoot,"a")
for h in n:
    www.write(h+" ")
www.close()
print("??")
ggg=open(DataRoot,"r")
gg=ggg.readline().split()
gg[6]="KOPWERKOP"
ggg.close()
ff=open(DataRoot,"w")
ff.write("")
ff.close()
fff=open(DataRoot,"a")

for a in gg:
    fff.write(a+" ")
FrontDoorMotor.open()
time.sleep(10)
FrontDoorMotor.close()'''
#Front.start()




            
    