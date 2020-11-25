import threading
import time
import RPi.GPIO as GPIO
import cv2 as cv
import find
import CutAndNet
import os
import stepmotorClass
import torch
import light
DataRoot=r"/home/pi/Desktop/work2/car-work/DataBase.pt"
CarInputRoot=r"/home/pi/Desktop/work2/car-work/data.txt"
GPIO.setwarnings(0)

m=stepmotorClass.m

fp=open(DataRoot,"r")
Seven=light.Segments
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
        if count>=9500:
            bMotor.ChangeDutyCycle(write(90))
            time.sleep(5)
            bMotor.ChangeDutyCycle(write(0))
'''

todo

在最一開始的時候讓他正轉一度在負轉一度 此時狀態在第一種 所以這時候內部變數要設定為1 也就是第二種

內部變數是用來判斷該走哪一步的

所以假設現在為0 代表要走第一種狀態 所以現在是在第四種狀態 要反轉就要走第三種狀態 也就是0-2+4

假設現在為a 要反轉之前就要先把a-2在+4(避免為負數) 迴圈內部要-1 

迴圈執行到一半的時候且還沒運轉時 如果內部變數等於-1 那就要把它+4'''

cnn=CutAndNet.CNN()
cnn.load_state_dict(torch.load("car-work/reallynet.pt"))
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
        #print(count,"A") #lefT
        if count>4000:
            while delay==999999:
                time.sleep(1)
            delay=99999
            print("請停止移動 稍後進行拍照及辨識")
            time.sleep(2)
            cap=cv.VideoCapture(0)
            ret,img=cap.read()
            cap.release()
            Find,img=find.lpr(img)
            
            if Find:
                fp=open(DataRoot,"r")
                x=fp.readline().split()
                fp.close()
                ans=CutAndNet.read(img,cnn)
                for w in range(8):
                    if x[w]=="None":
                        fMotor.ChangeDutyCycle(write(90))
                        time.sleep(5)
                        fMotor.ChangeDutyCycle(write(0))
                        time.sleep(3)
                        m.run(w*45,0.025)
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
GPIO.setup(btm,GPIO.IN)
while True:
    time.sleep(2)
    fp=open(CarInputRoot,"r")
    CarList=fp.readline().split()
    fp.close()
    while len(CarList)>0:
        
        delay=999999
        
        w=open(DataRoot,"r")
        n=w.readline().split()
        w.close()

        for f in range(8):
            if n[f]==CarList[0]:
                n[f]="None"
                m.run(180-45*f,0.025)
                count=n.count("None")
                Seven.ChangeState(count)
                break
    
        { 
           ww=open(DataRoot,"w")
           ww.write("")
           ww.close()
        }
        print(n)
        {
            fff=open(DataRoot,"a")
            for a in n:
                fff.write(a+" ")
            fff.close()            
        }


        {
            f=open(CarInputRoot,"w")
            f.write("")
            f.close()            
        }

        {
            CarList.clear()
            f=open(CarInputRoot,"a")
            for x in range(1,len(CarList)):
                f.write(x+" ")
                CarList.append(x)
            f.close()
        }

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




            
    