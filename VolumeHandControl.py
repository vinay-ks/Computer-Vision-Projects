import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import alsaaudio        # pip install pyalsaaudio    .......    Dependancy -> apt install libasound2-dev

# alsaaudio for linux    ......   pycaw for windows

#########################
wCam, hCam = 1000, 600
#########################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime, cTime = 0, 0

detector = htm.handDetector(detectionCon=0.7)

volobj = alsaaudio.Mixer()
minVol, maxVol = 0, 100
vol, volBar, volPer = 0, 400, 0


while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) !=0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2             # Middle point

        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # Hand Range        50 - 300
        # Volume Range      0  - 100
        vol = int(np.interp(length, [50,300], [minVol, maxVol]))
        volBar = int(np.interp(length, [50,300], [400, 150]))
        volPer = int(np.interp(length, [50,300], [0, 100]))
        print(vol)
        volobj.setvolume(vol)


        # For the green dot when volume is zero
        if length<50:
            cv2.circle(img, (cx,cy), 15, (0,255,0),cv2.FILLED)

    # Volume bar and percentage display
    cv2.rectangle(img, (50,150), (85, 400), (0,255,0), 3)
    cv2.rectangle(img, (50,volBar), (85, 400), (0,255,0), cv2.FILLED)
    cv2.putText(img, f'{volPer} %', (40,450), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)


    # Calculating FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    # Displaying FPS
    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)


    cv2.imshow("Img", img)
    cv2.waitKey(1)