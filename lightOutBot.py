'''
ลิ้งค์เกม http://www.logicgamesonline.com/lightsout/
กดรันรอบแรกปรับให้เห็นทั้งตาราง
ใส่comment บรรทัดที่ 91 เอาcomment บรรทัดที่ 77 - 89  ออก
กดรันรอบ2 เริ่มบอท
'''
import cv2
import numpy as np
import pyautogui
from operator import itemgetter

whiteColor = np.array([255 ,255 ,255])
grayColor = np.array([153 ,153 ,153])
image_width = 1440
image_height = 900
w = -1
h = -1
xRes = -1
yRes = -1
cout = 0

def printScreen():
    img = pyautogui.screenshot(
        region=(240, 240, int(image_width / 2)-240, image_height-240))
    img = np.array(img)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def findWhite(img):
    box = cv2.inRange(img, whiteColor, whiteColor)
    return box

def findAll(img):
    boxWhite = cv2.inRange(img, whiteColor, whiteColor)
    boxGray = cv2.inRange(img, grayColor, grayColor)
    return (boxWhite + boxGray)

def firstBox(img):
    xyList = []
    allBox = findAll(img)
    _, thresh = cv2.threshold(allBox, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, kernel = np.ones((5, 5), np.uint8), iterations = 1)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for c in contours :
        rect= cv2.minAreaRect(c)
        center, wh, angle = cv2.minAreaRect(c)
        x, y = center
        xyList.append([y,x])
        xyList = sorted(xyList, key=itemgetter(0,1))
        yRes, xRes = xyList[0]
        return xyList[0]

while True:
    xyList = []
    img = printScreen()
    if img is None:
        continue
    frame = img.copy()
    white = findWhite(img)
    _, thresh = cv2.threshold(white, 127, 255, cv2.THRESH_BINARY)
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
        xyList.append([y,x])
        xyList = sorted(xyList, key=itemgetter(0,1))
        yRes ,xRes = xyList[0]
    if xyList == [] :
        continue
    first_y, first_x = firstBox(img)
    '''
    if int(yRes) < int(first_y) + 10 and int(yRes) > int(first_y) - 10 :
        if int(xRes) > int(first_x) - 210 and int(xRes) < int(first_x) - 190 :
            pyautogui.click(x=int(xRes+150+240), y=int(yRes-200+240))
            pyautogui.click(x=int(xRes+200+240), y=int(yRes-200+240))
        elif int(xRes) > int(first_x) - 160 and int(xRes) < int(first_x) - 140 :
            pyautogui.click(x=int(xRes+240), y=int(yRes-200+240))
            pyautogui.click(x=int(xRes+150+240), y=int(yRes-200+240))
        elif int(xRes) > int(first_x) - 110 and int(xRes) < int(first_x) - 90 :
            pyautogui.click(x=int(xRes+50+240), y=int(yRes-200+240))
    else :
        pyautogui.click(x=int(xRes+240), y=int(yRes+50+240))
    '''
    cout += 1
    cv2.imshow('All', findAll(img.copy()))
    key = cv2.waitKey(1) & 0xff
    if cout >= 50:
        break
cv2.destroyAllWindows()
