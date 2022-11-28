import numpy as np
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import math
import random


class SnakeGame:
    def __init__(self,pathFood):
        self.points=[]
        self.lengths=[]
        self.currentLength=0
        self.allowedLength=500
        self.previousHead=0,0
        self.score=0

        self.imgFood=cv2.imread(pathFood,cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood,_=self.imgFood.shape
        self.foodPoint=0, 0
        self.randomFoodLocation()

    def randomFoodLocation(self):
        self.foodPoint=random.randint(100,1000),random.randint(100,600)


    def update(self,imgMain,currentHead):
        px,py=self.previousHead
        cx,cy=currentHead
        self.points.append([cx,cy])
        distance=math.hypot(cx-px,cy-py)
        self.lengths.append(distance)
        self.currentLength+=distance
        self.previousHead=cx,cy

        if self.currentLength>self.allowedLength:
            for i,length in enumerate(self.lengths):
                self.currentLength-=length
                self.lengths.pop(i)
                self.points.pop(i)
                if self.currentLength<self.allowedLength:
                    break


        rx,ry=self.foodPoint
        if rx - self.wFood//2<cx <rx+self.wFood//2 and ry-self.hFood//2 <cy<ry+self.hFood//2:
            print("Eating", self.score)
            self.randomFoodLocation()
            self.allowedLength+=50
            self.score+=1

        if self.points:
            for i,points in enumerate(self.points):
                if i!=0:
                    cv2.line(imgMain,self.points[i-1],self.points[i],(0,0,255),20)
            cv2.circle(imgMain,self.points[-1],20,(200,0,200),cv2.FILLED)

        
        imgMain=cvzone.overlayPNG(imgMain,self.imgFood,(rx-self.wFood//2,ry-self.hFood//2))
        return imgMain



cap=cv2.VideoCapture(0)

cap.set(3,1920)
cap.set(4,1080)
detector=HandDetector(detectionCon=0.8,maxHands=2)
game=SnakeGame("pizza.png")
while(True):
    success,img=cap.read()
    img=cv2.flip(img,1)
    hands,img=detector.findHands(img,flipType=False)

    if hands:
        lmList=hands[0]['lmList']
        pointIndex=lmList[8][0:2]
        img=game.update(img,pointIndex)
        

    cv2.imshow('Image',img)
    cv2.waitKey(1)
    12
345678