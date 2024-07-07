import cv2
import numpy as np
cam=cv2.VideoCapture(0)
# cam = cv2.VideoCapture(r"C:\Users\91987\OneDrive - IIT Kanpur\Desktop\Eclub\Y23 Sky Photo - View 2.png")
def Huelow(val):
    global HueLow
    HueLow=val

def Huehigh(val):
    global HueHigh
    HueHigh=val

def Satlow(val):
    global SatLow
    Satlow=val

def Sathigh(val):
    global SatHigh
    SatHigh=val

def Vallow(val):
    global ValLow
    ValLow=val

def Valhigh(val):
    global ValHigh
    ValHigh=val

threshmin=1
threshmax =1

def Max(val):
    global threshmax
    threshmax=val

def Min(val):
    global threshmin
    threshmin=val
    
def Area_c(val):
    global ar
    ar = val

HueHigh=0
HueLow=0
SatHigh=0
SatLow=0
ValLow=0
ValHigh=0
ar = 0

cv2.namedWindow('My frame')
cv2.createTrackbar('hueL','My frame',0,180,Huelow)
cv2.createTrackbar('hueH','My frame',0,180,Huehigh)

cv2.createTrackbar('satL','My frame',0,255,Satlow)
cv2.createTrackbar('satH','My frame',0,255,Sathigh)

cv2.createTrackbar('valL','My frame',0,255,Vallow)
cv2.createTrackbar('valH','My frame',0,255,Valhigh)

cv2.createTrackbar("Min",'My frame',1,255,Min)
cv2.createTrackbar("Max",'My frame',1,255,Max)

cv2.createTrackbar("Area",'My frame',1,1500,Area_c)

width = 700
height = 500

while True:
    ignore,frame = cam.read()
    # frame = cv2.imread(r"C:\Users\91987\OneDrive - IIT Kanpur\Desktop\Eclub\Y23 Sky Photo - View 2.png")
    frame = cv2.resize(frame,(700,500))
    # frame = cv2.flip(frame,1)
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    # cv2.moveWindow('my frame',0,0)
    lowerBound=np.array([HueLow,SatLow,ValLow])
    upperBound=np.array([HueHigh,SatHigh,ValHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)

    mySelection=cv2.bitwise_and(frame,frame, mask=myMask)
    mySelectiongray = cv2.cvtColor(mySelection,cv2.COLOR_BGR2GRAY)

    blur_gaussain = cv2.GaussianBlur(mySelectiongray,(7,7),1)
    ret,thresh = cv2.threshold(blur_gaussain,threshmin,threshmax,0)
    blur_median = cv2.medianBlur(thresh,7)
    frameDilate = cv2.dilate(blur_median,(7,7))
    blank= np.zeros(frame.shape,dtype=np.uint8)
    contours, hierarchies = cv2.findContours(frameDilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(blank , contours , -1 , (0,0,255),1)
    blank = cv2.GaussianBlur(blank,(7,7),1)
    blank = cv2.dilate(blank,(11,11))
    # ret,blank = cv2.threshold(blank,200,0,0)
    cv2.imshow("Contours",blank)
    # cv2.resizeWindow('my frame',width,height)
    
    cv2.imshow('My Selection',mySelection)
    cv2.imshow('Dilated',frameDilate)
    # cv2.resizeWindow('My Selection',width,height)
    # cv2.moveWindow('my frame',0,0)
    # cv2.moveWindow('My Selection',width+30,0)
    cv2.imshow('my frame',frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
# cam.release()
