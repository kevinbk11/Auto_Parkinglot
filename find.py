import cv2
import numpy as np
import time as t
def lpr(img):
    # 預處理，包括灰度處理，高斯濾波平滑處理，Sobel提取邊界，影象二值化
    # 對於高斯濾波函式的引數設定，第四個引數設為零，表示不計算y方向的梯度，原因是車牌上的數字在豎方向較長，重點在於得到豎方向的邊界
    # 對於二值化函式的引數設定，第二個引數設為127，是二值化的閾值，是一個經驗值
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    if len(gray_img)>2000:
          x1=gray_img.size
          y1=len(gray_img)
          z1=int(x1/y1)
          gray_img=cv2.resize(gray_img,(int(z1/4),int(y1/4)))
          img=cv2.resize(img,(int(z1/4),int(y1/4)))

    GaussianBlur_img = cv2.GaussianBlur(gray_img, (7, 7),5)
    GaussianBlur_img = cv2.medianBlur(GaussianBlur_img, 3)



    Sobel_img = cv2.Sobel(GaussianBlur_img, -1, 1, 0, ksize=3)
    Sobel_img2 = cv2.Sobel(GaussianBlur_img, -1, 0, 2, ksize=5)
    img_sobel = cv2.addWeighted(Sobel_img, 0.8, Sobel_img2, 0.2, 0)


    
    ret, binary_img = cv2.threshold(img_sobel, 90, 255, cv2.THRESH_BINARY)
   
    # 形態學運算
    kernel = np.ones((30, 55), np.uint8)
    
    # 先閉運算將車牌數字部分連線，再開運算將不是塊狀的或是較小的部分去掉
    close_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

    open_img = cv2.morphologyEx(close_img, cv2.MORPH_OPEN, kernel)
    close_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

    # kernel2 = np.ones((10, 10), np.uint8)
    # open_img2 = cv2.morphologyEx(open_img, cv2.MORPH_OPEN, kernel2)
    # 由於部分影象得到的輪廓邊緣不整齊，因此再進行一次膨脹操作
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilation_img = cv2.dilate(open_img, element, iterations=3)

    # 獲取輪廓
    contours, hierarchy = cv2.findContours(dilation_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 測試邊框識別結果
    #cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
    #cv2.imshow("lpr", img)
    #cv2.waitKey(0)

    # 將輪廓規整為長方形
    rectangles = []
    for c in contours:
        x = []
        y = []
        for point in c:
            y.append(point[0][0])
            x.append(point[0][1])
        r = [min(y), min(x), max(y), max(x)]
        rectangles.append(r)

    # 用顏色識別出車牌區域0
    # 需要注意的是這裡設定顏色識別下限low時，可根據識別結果自行調整
    dist_r = []
    In=False
    max_mean = 0
    for r in rectangles:
        block = img[r[1]:r[3], r[0]:r[2]]
        x=int(block.size/len(block))
        y=int(block.size/x)
        if(x*y<10000):
              continue
        if(x/y<4):continue
        hsv = cv2.cvtColor(block, cv2.COLOR_BGR2HSV)
        low = np.array([0,50,50])
        up = np.array([150,255,255])
        result = cv2.inRange(hsv, low, up)
        
        # 用計算均值的方式找藍色最多的區塊

        mean = cv2.mean(result)
        if mean[0] > max_mean:
            max_mean = mean[0]
            dist_r = r
            In=True
    # 畫出識別結果，由於之前多做了一次膨脹操作，導致矩形框稍大了一些，因此這裡對於框架+3-3可以使框架更貼合車牌
    
    if(In):
        cutimg=img[dist_r[1]-5:dist_r[3]-5,dist_r[0]+15:dist_r[2]+5]
        cutimg=cv2.cvtColor(cutimg,cv2.COLOR_BGR2GRAY)
        _,cutimg=cv2.threshold(cutimg,128,255,cv2.THRESH_BINARY)
        cv2.imshow("OWO",cutimg)
        cv2.waitKey(0)
        y=len(cutimg)#row
        m=y//2
        
        f=False
        R,L,U,D=0,0,0,0
        x=cutimg.size//y#column
        
        '''for cc in range(0,x):
            for c in range(0,y):
                if cutimg[c][cc] == 0:
                    print(cc)
                    L=cc
                    f=True
                    break
            if f:
                break'''
        for c in range(m,0,-1):
            black=0
            for cc in range(0,x):
                if cutimg[c][cc]==0:
                    black+=1
            if black<=10:
                U=c
                break
        try:
            cutimg=cutimg[U:,:]
        except:
            print("?")
        return True,cutimg
    else:
        return False,None
