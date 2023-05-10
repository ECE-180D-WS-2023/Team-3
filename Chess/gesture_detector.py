import cv2 
import cvzone
import time
import random

from cvzone.HandTrackingModule import HandDetector

def gesture_cap():
    cap = cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    detector = HandDetector(maxHands=1)
    initialTime = time.time()

    success, img = cap.read()
    imgScaled = cv2.resize(img, (0,0), None, 0.375, 0.375)

    hands, img = detector.findHands(imgScaled)

    gesture = "NA"

    while time.time() - initialTime < 3:
        if hands:
            hand = hands[0]
            fingers = detector.fingersUp(hand)
            if fingers == [0,1,0,0,0]:
                gesture = "y"
            elif fingers == [0,1,1,0,0]:
                gesture = "n"
    return gesture