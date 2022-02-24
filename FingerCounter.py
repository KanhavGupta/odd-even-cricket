import os
import random
import numpy as np
import cv2
import time
import HandTrackingModule as htm

############################
wCam, hCam = 1280, 720
############################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

folderPath = "numbers"
myList = os.listdir(folderPath)
imagesList = []
for ipath in myList:
    image = cv2.imread(f'{folderPath}/{ipath}')
    imagesList.append(image)

detector = htm.HandDetector(detection_con=0.8)
tipIds = [4, 8, 12, 16, 20]
op = -1
batting = [0, 0]
meBat = True
display = ""
final_dis = ""
while True:
    img = np.ones((720,1280,3))
    cv2.putText(img, ">Press r to restart",
                (20,40),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.putText(img, ">Press q to quit",
                (20,80),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.putText(img, ">Press p for CPUs number",
                (20,120),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.putText(img, ">Press s to start game",
                (20,160),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.imshow("image",img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

while True:
    success, img = cap.read()
    img = detector.findHands(img,draw=False)
    lmList = detector.findPosition(img, draw=False)

    me = 0
    cv2.putText(img, "YOU",(60,250),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv2.putText(img, "CPU",(1150,250),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),3)
    cv2.putText(img, "VS",(600,100),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),3)
    img[0:200, 0:200] = imagesList[10]
    if len(lmList) != 0:
        fingers = []
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totFingers = fingers.count(1)
        w, h = 200, 200
        if fingers[1] == 1 and fingers.count(1) == 1:
            me = 1
            img[0:h, 0:w] = imagesList[1]
        elif fingers[1] == 1 and fingers[2] == 1 and fingers.count(1) == 2:
            me = 2
            img[0:h, 0:w] = imagesList[2]
        elif fingers[0] == 0 and fingers[4] == 0 and fingers.count(1) == 3:
            me = 3
            img[0:h, 0:w] = imagesList[3]
        elif fingers[0] == 0 and fingers.count(1) == 4:
            me = 4
            img[0:h, 0:w] = imagesList[4]
        elif fingers.count(1) == 5:
            me = 5
            img[0:h, 0:w] = imagesList[5]
        elif fingers.count(0) == 5:
            me = 10
            img[0:h, 0:w] = imagesList[0]
        elif fingers[0]==1 and fingers.count(1) == 1:
            me = 6
            img[0:h, 0:w] = imagesList[6]
        elif fingers[0]==1 and fingers[1]==1 and fingers.count(1) == 2:
            me = 7
            img[0:h, 0:w] = imagesList[7]
        elif fingers[3]==0 and fingers[4]==0 and fingers.count(1) == 3:
            me = 8
            img[0:h, 0:w] = imagesList[8]
        elif fingers[4]==0 and fingers.count(1) == 4:
            me = 9
            img[0:h, 0:w] = imagesList[9]

    # cTime = time.time()
    # fps = 1/(cTime-pTime)
    # pTime = cTime
    # cv2.putText(img, f'FPS: {(int(fps))}', (480,50), cv2.FONT_HERSHEY_COMPLEX, 1,
    #             (255,0,0), 3)

    if cv2.waitKey(1) & 0xFF == ord('p'):
        op = random.randint(0,9)

        if meBat:
            if (op == 0 and me == 10) or op == me:
                display = "OUT"
                meBat = False
            else:
                batting[0]+=me
                display = f"{me}"
        else:
            if (op == 0 and me == 10) or op == me :
                display = "OUT"
                if batting[0] > batting[1]:
                    final_dis = "YOU WON"
                elif batting[0] == batting[1]:
                    final_dis = "Draw"
            else:
                if op == 0:
                    batting[1]+=10
                else:
                    batting[1]+=op
                if batting[0] < batting[1]:
                    final_dis = "CPU WON"
                display = f"{op}"
    # central display
    cv2.putText(img, display,(615,150),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),3)
    # Your Display
    cv2.putText(img, f"{batting[0]}",(220,30),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),3)
    # CPU display
    cv2.putText(img, f"{batting[1]}",(1000,30),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),3)
    # final display
    cv2.putText(img, f"{final_dis}",(540,360),cv2.FONT_HERSHEY_PLAIN,5,(255,255,0),3)
    img[0:200, wCam-200:wCam] = imagesList[op]
    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord('r'):
        op = -1
        batting = [0, 0]
        meBat = True
        display = ""
        final_dis = ""
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
