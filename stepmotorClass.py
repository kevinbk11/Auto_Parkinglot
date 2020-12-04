import sys
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
class stepmotor():
  def __init__(self,a,b,abar,bbar):
    self.Now=0
    GPIO.setup(a,GPIO.OUT)
    GPIO.setup(b,GPIO.OUT)
    GPIO.setup(abar,GPIO.OUT)
    GPIO.setup(bbar,GPIO.OUT)
    self.a=a
    self.b=b
    self.abar=abar
    self.bbar=bbar
  def run(self,theta,speed,ZeroFlag):

    if theta>=360:
      theta%=360
    step=round((theta/1.8),1)
    for r in range(int(step)):


        if self.Now%4==0:
          GPIO.output(self.a,0)
          GPIO.output(self.b,1)
          GPIO.output(self.abar,1) 
          GPIO.output(self.bbar,0)  
        if self.Now%4==1:
          GPIO.output(self.a,0)
          GPIO.output(self.b,1)
          GPIO.output(self.abar,0)
          GPIO.output(self.bbar,1)
        if self.Now%4==2:
          GPIO.output(self.a,1)
          GPIO.output(self.b,0)
          GPIO.output(self.abar,0)
          GPIO.output(self.bbar,1)
        if self.Now%4==3:
          GPIO.output(self.a,1)
          GPIO.output(self.b,0)
          GPIO.output(self.abar,1)
          GPIO.output(self.bbar,0)
        self.Now+=1
        time.sleep(speed)
    if theta!=0 and ZeroFlag!=True:
      time.sleep(4)
      self.run(360-theta,speed,True)

m=stepmotor(6,13,19,26)