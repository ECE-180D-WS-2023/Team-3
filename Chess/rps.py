import cv2 
import cvzone
import time
import random

from cvzone.HandTrackingModule import HandDetector

cap=cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

detector= HandDetector(maxHands=1)
startGame=True# can be set to true once a piece is captured
stateResult=False
initialTime=time.time()

while True:

    success, img =cap.read()
    imgScaled=cv2.resize(img,(0,0), None,0.375,0.375)
    
    hands, img= detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer=time.time()-initialTime  

            if timer>3:
                stateResult=True
                timer=0
        
                if hands:
                    hand=hands[0]
                    fingers=detector.fingersUp(hand)
                    #print(fingers)
                    if fingers==[0,0,0,0,0]:
                        playerMove="Rock"
                    if fingers==[1,1,1,1,1]:
                        playerMove="Paper"                        
                    if fingers==[0,1,1,0,0]:
                        playerMove="Scissors"

                    options = "rock", "paper", "scissors"
                    ai_pick=random.choice(options)
                    print("ai picked", ai_pick)

                    print(playerMove)


    cv2.imshow("Image", imgScaled)
    cv2.waitKey(1)