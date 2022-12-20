import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

wcam, hcam = 640, 480
frameR = 100
smooth = 7
plx, ply = 0,0
clx, xly = 0,0

cap = cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)
pT = 0
detector = htm.handDetector(maxHands=1)
wS, hS = autopy.screen.size()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmL, bbox = detector.findPosition(img)
    if len(lmL)!=0:
        x1, y1 = lmL[8][1:]
        x2, y2 = lmL[12][1:]

    fingers = detector.fingersUp()
    cv2.rectangle(img, (frameR,frameR), (wcam-frameR, hcam-frameR), (255,0,255), 2)
    if fingers[1]==1 and fingers[2]==0:

      x3 = np.interp(x1, (frameR,wcam-frameR), (0, wS))
      y3 = np.interp(y1, (frameR,hcam-frameR), (0, hS))
      clx = plx + (x3 - plx)/ smooth
      cly = ply + (y3 - ply) / smooth
      autopy.mouse.move(wS-clx, cly)
      cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
      plx, ply  = clx, cly
    if fingers[1] == 1 and fingers[2] == 1:
        length, img, lineInfo = detector.findDistance(8,12,img)
        if length<40:
            cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0,255,0), cv2.FILLED)
            autopy.mouse.click()

    cT = time.time()
    fps = 1/(cT-pT)
    pT=cT
    cv2.putText(img, str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,
                (255,0,0), 3
                )
    cv2.imshow("Image", img)
    cv2.waitKey(1)
