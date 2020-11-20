import RPi.GPIO as GPIO
class seg():
    def __init__(self,D,C,B,A):
        self.__Pin=[D,C,B,A]
        self.__StateTable=[
            [0,0,0,0],
            [0,0,0,1],
            [0,0,1,0],
            [0,0,1,1],
            [0,1,0,0],
            [0,1,0,1],
            [0,1,1,0],
            [0,1,1,1],
            [1,0,0,0]
        ]
        
        GPIO.setup(D,GPIO.OUT)
        GPIO.setup(C,GPIO.OUT)
        GPIO.setup(B,GPIO.OUT)
        GPIO.setup(A,GPIO.OUT)
        
    def ChangeState(self,N):
        NewState=self.__StateTable[N]
        r=0
        for pin in self.__Pin:
            GPIO.output(pin,NewState[r])
            r+=1
Segments=seg(23,24,25,8)