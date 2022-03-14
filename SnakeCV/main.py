import numpy as np
import cv2
import mediapipe

cap=cv2.VideoCapture(0)

cap.set(3,1920)
cap.set(4.1080)
detector=HandDetector(detectionCon=0.8,maxHands=1)
while(True):
    success,img=cap.read()
    hands,img=detector.findHands(img)
    cv2.imshow('Image',img)
    cv2.waitKey(1)