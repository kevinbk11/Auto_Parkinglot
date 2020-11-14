import cv2
import torch
import torch.nn as nn
import torch.utils.data as Data
import torchvision
from torchvision import transforms
import numpy as np
import matplotlib.pyplot as plt
import random as rand
CharDict={1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"0",11:"A",
          12:"B",13:"C",14:"D",15:"E",16:"F",17:"G",18:"H",19:"1",20:"J",21:"K",
          22:"L",23:"M",24:"N",25:"0",26:"P",27:"Q",28:"R",29:"S",30:"T",31:"U",
          32:"V",33:"W",34:"X",35:"Y",36:"Z"}
class CNN(nn.Module):
        def __init__(self):
            super(CNN,self).__init__()
            self.conv1 = nn.Sequential(
                nn.Conv2d( # 1 56 56
                    in_channels=1,
                    out_channels=16,
                    kernel_size=5,
                    stride=1,
                    padding=2,
                ),
                nn.MaxPool2d(4,4), #16 14 14
                nn.ReLU(inplace=True)
            )
            self.conv2=nn.Sequential(                
                nn.Conv2d(16,36,5,1,2),
                nn.BatchNorm2d(36),
                nn.MaxPool2d(2,2), #36 7 7
                nn.ReLU(inplace=True),
            )
            self.out =nn.Sequential(           
                nn.Linear(36*7*7,128),
                nn.ReLU(True),
                nn.Linear(128,37),
            ) 
        def forward(self,x):
            x=self.conv1(x)
            x=self.conv2(x)
            x=x.view(x.size(0),-1)
            output = self.out(x)
            return output,x
def read(inimg,cnn):
    # 1、读取图像，并把图像转换为灰度图像并显示
    print("Wait...")
    img_gray = inimg  # 读取图片
    #img = cv2.GaussianBlur(img,(5,5),3)
    #img = cv2.pyrMeanShiftFiltering(img, 35, 100);
    #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # 转换了灰度化
    #cv2.waitKey()
    y=img_gray.size
    x=int(len(img_gray))
    differ=int(y/x/4)
    if(differ>1000 and x >1000):
        img_gray=cv2.resize(img_gray ,(differ,int(x/4)))

    
    # 2、将灰度图像二值化，设定阈值是100
    img_thre = img_gray
    cv2.threshold(img_gray, 140, 255, cv2.THRESH_BINARY, img_thre)


    # 3、保存黑白图片

    
    # 4、分割字符
    white = []  # 记录每一列的白色像素总和
    black = []  # ..........黑色.......
    height = img_thre.shape[0]
    width = img_thre.shape[1]
    white_max = 0
    black_max = 0
    # 计算每一列的黑白色像素总和
    for i in range(width):
        s = 0  # 这一列白色总数
        t = 0  # 这一列黑
        for j in range(height):
            if img_thre[j][i] == 255:
                s += 1
            if img_thre[j][i] == 0:
                t += 1
        white_max = max(white_max, s)
        black_max = max(black_max, t)
        white.append(s)
        black.append(t)
    
    arg = False  # False表示白底黑字；True表示黑底白字
    if black_max > white_max:
        arg = True
    
    # 分割图像
    def find_end(start_):
        end_ = start_+1
        for m in range(start_+1, width-1):
            if (black[m] if arg else white[m]) > (0.95 * black_max if arg else 0.95 * white_max):  # 0.95这个参数请多调整，对应下面的0.05
                end_ = m
                break
        return end_
    
    n = 1
    start = 1
    end = 2
    ans=""
    times=0
    while n < width-2:
        n += 1
        if (white[n] if arg else black[n]) > (0.05 * white_max if arg else 0.05 * black_max):
            # 上面这些判断用来辨别是白底黑字还是黑底白字
            # 0.05这个参数请多调整，对应上面的0.95
            start = n
            end = find_end(start)
            n = end
            if end-start > 5:
                cj = img_thre[1:height, start:end]
                cjs=len(cj)
                cjs3=cj.size
                try:
                    cjs2=cjs3/cjs
                except ZeroDivisionError:
                    return ""       
                resize=abs(int((cjs-cjs2)/2))
                cj=np.pad(cj,((0,0),(resize,resize)),'constant',constant_values = (255,255))
                cj=cv2.resize(cj,(56,56))
                #cj=np.pad(cj,((6,6),(6,6)),'constant',constant_values = (255,255))
                b=0
                w=0
                for x in cj:
                    for y in x:
                        if y>128:w+=1
                        if y<128:b+=1
                if(b<70):continue    
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))         
                up,down,right,left=0,0,0,0
                _,cj=cv2.threshold(cj,128,255,cv2.THRESH_BINARY)
                for xx in range(0,56):
                    if 0 in cj[xx]:
                        up=xx
                        for yy in range(xx+1,56):
                            if 0 not in cj[yy]:
                                down=yy
                                break
                        break
                f=False
                for aa in range(0,56):
                    na=cj[:,aa:aa+1]
                    if 0 in na:
                        left=aa
                        for bb in range(aa+1,56):
                            na=cj[:,bb:bb+1]
                            if 0 not in na:
                                right=bb
                                break
                        break
                #print(up,down,left,right)
                if down==0:down=-1
                cj=cj[up:down,left:right]
                cjs=len(cj)
                cjs3=cj.size 
                try:
                    cjs2=cjs3/cjs
                except ZeroDivisionError:
                    return ""
                resize=abs(int((cjs-cjs2)/2))
                cj=np.pad(cj,((0,0),(resize,resize)),'constant',constant_values = (255,255))
                cj=cv2.resize(cj,(44,44))
                cj=np.pad(cj,((6,6),(6,6)),'constant',constant_values = (255,255))
                cj=torch.from_numpy(cj)
                cj= (cj.view(1,1,56,56)/255.)

                test_output, _ = cnn(cj) 
                pred_y = torch.max(test_output, 1)[1].data.numpy()
                for x in pred_y:
                    ans=ans+CharDict[int(x)]
                    print(CharDict[int(x)],end="")
                times+=1
                if times>=7:
                    return ans
    return ans
