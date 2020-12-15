import threading
import time
import RPi.GPIO as GPIO
import cv2 as cv
import find
import CutAndNet
import os
import stepmotorClass
import torch
import SevenSegmentsClass
DataRoot=r"/home/pi/Desktop/work2/car-work/DataBase.pt"
CarInputRoot=r"/home/pi/Desktop/work2/car-work/data.txt"


GPIO.setwarnings(0)

m=stepmotorClass.m

fp=open(DataRoot,"r")
Seven=SevenSegmentsClass.Segments
x=fp.readline().split()
r=0
for h in x:
    if h=="None":
        r+=1
print(r)
Seven.ChangeState(r)
fp.close() 

def write(angle=0):
    duty_cycle = (0.05 * 50) + (0.19 * 50 * angle / 180)
    return duty_cycle

MONITOR_PIN = 2
MONITOR_PIN1 = 5
frontDoorPin=17
backDoorPin=22
btm = 15
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
fMotor=GPIO.PWM(17,50)
bMotor=GPIO.PWM(22,50)
fMotor.start(0)
bMotor.start(0)
time.sleep(2)
global delay
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
        #print(count) #right
        if count>=25000:
            bMotor.ChangeDutyCycle(write(90))
            time.sleep(5)
            bMotor.ChangeDutyCycle(write(0))

cnn=CutAndNet.CNN()
cnn.load_state_dict(torch.load("/home/pi/Desktop/work2/car-work/reallynet.pt"))
def FrontDoor():
    global delay
    while True:
        GPIO.setup(MONITOR_PIN, GPIO.OUT)
        GPIO.output(MONITOR_PIN, GPIO.LOW)
        time.sleep(0.1)

        count = 0
        GPIO.setup(MONITOR_PIN, GPIO.IN)
        while (GPIO.input(MONITOR_PIN) == GPIO.LOW):
            
            count += 1
        print(count,"A") #lefT

        if count>5000:
            full=False

            fp=open(DataRoot,"r")
            x=fp.readline().split()
            fp.close()
            Find=False

            while delay==999999:
                time.sleep(1)

            if x.count("None")==0:
                print("full")
                full=True
                
            delay=99999
            if not full:
                print("請停止移動 稍後進行拍照及辨識")
                time.sleep(2)
                cap=cv.VideoCapture(0)
                ret,img=cap.read()
                cap.release()
                Find,img=find.lpr(img)

        

            if Find and not full:
                ans=CutAndNet.read(img,cnn)
                if ans=="N":
                    break
                for w in range(8):
                    if x[w]=="None":
                        fMotor.ChangeDutyCycle(write(90))
                        time.sleep(5)
                        fMotor.ChangeDutyCycle(write(0))
                        time.sleep(3)

                        m.run(w*45,0.05,False)


                        x[w]=ans
                        break
                Seven.ChangeState(x.count("None"))
                ff=open(DataRoot,"w")
                ff.write("")
                ff.close()
                fff=open(DataRoot,"a")
                for a in x:
                    fff.write(a+" ")
                fff.close()
                cv.destroyAllWindows()
                delay=0
            delay=0

        
    
Front=threading.Thread(target=FrontDoor)
Back=threading.Thread(target=BackDoor)
Front.start()
Back.start()
global CarList
def CheckQueue():
    global CarList
    while True:
        time.sleep(0.025)
        fp=open(CarInputRoot,"r")
        x=fp.readline().split()
        if len(x)>0:
            CarList=x
        else:
            CarList=[" "]
        fp.close()
Check=threading.Thread(target=CheckQueue)
Check.start()
while True:
    time.sleep(2)
    while len(CarList)>0:
        if CarList[0]==" ":
            delay=0
            break
        delay=999999
        
        w=open(DataRoot,"r")
        n=w.readline().split()
        w.close()

        for f in range(8):
            if n[f]==CarList[0]:
                n[f]="None"

                m.run(180+45*f,0.03,False)

                count=n.count("None")
                Seven.ChangeState(count)
                break
        ww=open(DataRoot,"w")
        ww.write("")
        ww.close()


        fff=open(DataRoot,"a")
        for a in n:
            fff.write(a+" ")
        fff.close()
        f=open(CarInputRoot,"w")
        f.write("")
        f.close()
        
        oldCarList=CarList.copy()
        CarList.clear()
        f=open(CarInputRoot,"a")
        for x in range(1,len(oldCarList)):
            if x==len(oldCarList)-1:
                f.write(oldCarList[x])
            else:
                f.write(oldCarList[x]+" ")
            CarList.append(oldCarList[x])
        f.close()
    
    delay=0
