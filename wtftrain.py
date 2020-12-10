import os
import torch
import torch.nn as nn
import torch.utils.data as Data
import torchvision
import torch.functional as F
import torchvision.models as models
import cv2
import math
from torch.utils.data import DataLoader,Dataset
from skimage import io,transform
import matplotlib.pyplot as plt
from torchvision import transforms
from torch.optim.lr_scheduler import StepLR
import numpy as np
import time as t
EPOCH=1
BATCH_SIZE=32
LR=0.00025#0.00025 #0.0015
DOWNLOAD_MNIST=False

class DataSet(Dataset): #继承Dataset
    def __init__(self, root_dir, transform=None): #__init__是初始化该类的一些基础参数
        self.root_dir = root_dir   #文件目录
        self.transform = transform #变换
        self.images = os.listdir(self.root_dir)#目录里的所有文件
    
    def __len__(self):#返回整个数据集的大小
        return len(self.images)
    
    def __getitem__(self,index):#根据索引index返回dataset[index]
        image_index = self.images[index]#根据索引index获取该图片
        img_path = os.path.join(self.root_dir, image_index)#获取索引为index的图片的路径名143 271
        cj = cv2.imread(img_path)# 读取该图片/
        cj=cv2.cvtColor(cj,cv2.COLOR_BGR2GRAY)
        useless,cj=cv2.threshold(cj,128,255,cv2.THRESH_BINARY)
        cjs=len(cj)
        cjs3=cj.size 
        cjs2=cjs3/cjs
        resize=abs(int((cjs-cjs2)/2))
        cj=np.pad(cj,((0,0),(resize,resize)),'constant',constant_values = (255,255))
        cj=cv2.resize(cj,(20,20))
        cj=np.pad(cj,((4,4),(4,4)),'constant',constant_values = (255,255))
        img=cj
        cv2.imshow("t",img)
        cv2.waitKey(1)
        img=torch.from_numpy(img)
        img=img.view(1,28,28)
        label = img_path.split('\\')[-1].split('.')[0]# 根据该图片的路径名获取该图片的label，具体根据路径名进行分割。我这里是"E:\\Python Project\\Pytorch\\dogs-vs-cats\\train\\cat.0.jpg"，所以先用"\\"分割，选取最后一个为['cat.0.jpg']，然后使用"."分割，选取[cat]作为该图片的标签
        sample = {'image':img/255.,'label':int(label)}#根据图片和标签创建字典
        if self.transform:
            sample = self.transform(sample)#对样本进行变换
        return sample #返回该样本
data = DataSet(r"C:\Users\User\TEST\newcut",transform=None)

train_loader = Data.DataLoader(dataset=data, batch_size=BATCH_SIZE, shuffle=True)

class CNN(nn.Module):
        def __init__(self):
            super(CNN,self).__init__()
            self.conv1 = nn.Sequential(
                nn.Conv2d( # 1 56 56
                    in_channels=1,
                    out_channels=32,
                    kernel_size=5,
                    stride=1,
                    padding=2,
                ),
                nn.MaxPool2d(2,2), #32 14 14
                nn.ReLU(inplace=True)
            )
            self.conv2=nn.Sequential(               
                nn.Conv2d(32,64,5,1,2),
                nn.MaxPool2d(2,2), #64 7 7
                nn.BatchNorm2d(64), 
                nn.ReLU(inplace=True),
            )
            self.out =nn.Sequential(           
                nn.Linear(64*7*7,160),
                nn.ReLU(True),
                nn.Linear(160,37),
            ) 
        def forward(self,x):
            x=self.conv1(x)
            x=self.conv2(x)
            x=x.view(x.size(0),-1)
            output = self.out(x)
            return output,x
def save(): 
    cnn=CNN() #定義CNN的名稱為cnn
    CNN1=models.AlexNet()
    k=0
    h = list(cnn.parameters())
    for i in h:
        l = 1
        print("该层的结构：" + str(list(i.size())))
        for j in i.size():
            l *= j
        print("该层参数和：" + str(l))
        k = k + l
    print("总参数数量和：" + str(k))
    bk=False
    acc=0
    count=0
    right=0
    LastLoss=100
    for epoch in range(90):
        LR=0.0005#0.00025 #0.0015
        if LastLoss>3:
            LR=0.001
        elif LastLoss<3 and LastLoss>0.5:
            LR=0.001
        elif LastLoss<=0.5:
            LR=0.0005
        print(LR)
        print(epoch)
        if bk:break
        for i,b_x in enumerate(train_loader):
            LR=LR#*abs(math.cos((math.pi)-(i*5*math.pi/180)))
            print(i*5)
            optimizer=torch.optim.Adam(cnn.parameters(),lr=LR) #優化器 在此選擇Adam 學習率=0.001
            loss_func = nn.CrossEntropyLoss() #損失函數
            output = cnn(b_x['image'])[0]#將照片丟給cnn運算
            loss = loss_func(output,b_x['label'])#計算損失誤差 
            optimizer.zero_grad()#將梯度歸零
            loss.backward()#反向求函數偏導數
            optimizer.step()#更新權重
            Recognition_result=torch.max(output,1)[1]#取得當前判斷結果
         #   ans=str(int(b_x['label']))#取得答案
        #    count+=1
        #    if Recognition_result==ans:
        #        right+=1
            #print("訓練第 "+str(count)+" 次的結果="+str(Recognition_result),"正確答案="+ans,"ACC=%.3f"%(right/count))
            print(Recognition_result,b_x['label'])
            print(loss.data.numpy())
            LastLoss=loss.data.numpy()
    torch.save(cnn.state_dict(), 'reallynet1.pt')#訓練完成後將權重打包
    print("DONE")
save()