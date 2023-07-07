import cv2
import mediapipe as mp
import time

import numpy as np

import HandRecognitionModule as Hr
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#############################
wCam ,hCam = 640 ,480
#############################

cap = cv2.VideoCapture(0)
cap.set(3 , wCam)
cap.set(4 , hCam)
pTime =0
vol =0
volBar =400
volPer =0
detector = Hr.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]




while True:
    success , img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img , draw=False)
    if len(lmList) != 0:
        #print(lmList[4] , lmList[8])
        x1 , y1 = lmList[4][1] , lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx , cy = (x1 +x2)//2 , (y1 + y2)//2
        cv2.circle(img , (x1,y1) , 10 ,(0,255,0) , cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
        cv2.line(img , (x1 ,y1) , (x2 , y2) , (0, 255 , 0) , 3)
        cv2.circle(img, (cx, cy), 10, (255, 100, 0), cv2.FILLED)

        lenn = math.hypot(x2-x1 , y2-y1)
        #print(lenn)
        #hand range was 50 to 250
        #vol range = -65 to 0

        vol = np.interp(lenn , [50 ,250] ,[minVol,maxVol])
        volBar = np.interp(lenn, [50, 250], [400, 150])
        volPer = np.interp(lenn, [50, 250], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)

        if lenn < 50:
            cv2.circle(img, (cx, cy), 10, (0, 100, 255), cv2.FILLED)


    cv2.rectangle(img , (50,150), (85,400) ,(0,255,0), 3)
    cv2.rectangle(img, (50, int(volBar )), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cTime = time.time()
    fps= 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img , f'FPS = {int(fps)}' , (40 ,50) , cv2.FONT_HERSHEY_PLAIN , 2 ,(255,0,0) ,2 )
    cv2.imshow("Image" , img)
    cv2.waitKey(1)