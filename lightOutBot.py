import cv2
import numpy as np
import pyautogui
from operator import itemgetter

image_width = 1440
image_height = 900
w = -1
h = -1

def printScreen():
    img = pyautogui.screenshot(
        region=(240, 240, int(image_width / 2)-240, image_height-240))
    img = np.array(img)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def findBox(img):
    white = np.array([255 ,255 ,255])
    box = cv2.inRange(img, white, white)
    return box


while True:
    xyList = []
    img = printScreen()
    if img is None:
        continue
    frame = img
    img = findBox(img)
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, kernel = np.ones((5,5),np.uint8), iterations = 1)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for c in contours :
        rect= cv2.minAreaRect(c)
        center, wh, angle = cv2.minAreaRect(c)
        x, y = center
        w, h = wh
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        frame = cv2.drawContours(frame,[box],0,(0,0,255),2)
        xyList.append([x,y])
        xyList = sorted(xyList, key=itemgetter(1))
        xRes, yRes = xyList[0]
    print('res',xyList)
             
    cv2.imshow('box',thresh)
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
cv2.destroyAllWindows()