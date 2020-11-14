import threading
import time
import RPi.GPIO as GPIO
import cv2 as cv
import find
import CutAndNet
import os

def write(angle=0):
    duty_cycle = (0.05 * 50) + (0.19 * 50 * angle / 180)
    return duty_cycle

DataRoot=r"/home/pi/Desktop/work2/car-work/DataBase.pt"
MONITOR_PIN = 2
MONITOR_PIN1 = 5
frontDoorPin=17
backDoorPin=22
btm = 7
cap=cv.VideoCapture(0)
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
            if count>=50000:break
        print(count)
        if count>=50000:
            bMotor.ChangeDutyCycle(write(90))
            time.sleep(5)
            bMotor.ChangeDutyCycle(write(0))
'''

todo

在最一開始的時候讓他正轉一度在負轉一度 此時狀態在第一種 所以這時候內部變數要設定為1 也就是第二種

內部變數是用來判斷該走哪一步的

所以假設現在為0 代表要走第一種狀態 所以現在是在第四種狀態 要反轉就要走第三種狀態 也就是0-2+4

假設現在為a 要反轉之前就要先把a-2在+4(避免為負數) 迴圈內部要-1 

迴圈執行到一半的時候且還沒運轉時 如果內部變數等於-1 那就要把它+4

'''
#cnn=CutAndNet.CNN()
#cnn.load_state_dict()
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
        #print(count,"A")
        if count>1800:
            '''if delay==999999:
                print("有人正在取車,請稍後")
                while delay==999999:
                    print(".")
                    time.sleep(1)
            delay=99999
            print("請停止移動 稍後進行拍照  及辨識")
            time.sleep(5)
            ret,img=cap.read()
            Find,img=find.lpr(img)
            if Find:
                fp=open(DataRoot,"r")
                x=fp.readline().split()
                fp.close()
                ans=CutAndNet.read(img,cnn)
                for w in range(8):
                    if x[w]=="None":
                        #馬達要轉轉
                        x[w]=ans
                ff=open(DataRoot,"w")
                ff.write()
                ff.close()
                fff=open(DataRoot,"a")
                for a in x:
                    ff.write(a+" ")
                delay=0'''
            fMotor.ChangeDutyCycle(write(90))
            time.sleep(5)
            fMotor.ChangeDutyCycle(write(0))
            
            
        time.sleep(delay)
    
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
        if delay==99999:
            print("有人正在停車,請稍後")
            while delay==99999:
                print(".")
                time.sleep(1)
        delay=999999
        x = input()
        w=open(DataRoot,"r")
        n=w.readline().split()
        for f in range(8):
            if n[f]==x:
                n[f]="None"
                #馬達要轉轉
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




            
    