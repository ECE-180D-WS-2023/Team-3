
import time
import cv2 as cv
import numpy as np
from sklearn.cluster import KMeans 
cap = cv.VideoCapture(1, cv.CAP_DSHOW)
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
#cap = cv.VideoCapture(0)

current_player=1
had_both=False
printed=False
initial_time=1 #min

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = None
        self.remaining_time = duration

    def start(self):
        if self.start_time is None:
            self.start_time = time.monotonic()
        else:
            self.start_time = time.monotonic() - self.remaining_time

    def pause(self):
        if self.start_time is not None:
            self.remaining_time = time.monotonic() - self.start_time
            self.start_time = None

    def resume(self):
        if self.start_time is None:
            self.start_time = time.monotonic() - self.remaining_time

    def reset(self):
        self.start_time = None
        self.remaining_time = self.duration

    def time_remaining(self):
        if self.start_time is None:
            return self.remaining_time
        else:
            elapsed_time = time.monotonic() - self.start_time
            remaining_time = self.duration - elapsed_time
            return max(0, remaining_time)

class ChessTimer:
    def __init__(self, initial_time):
        self.initial_time = initial_time
        self.time_left = [initial_time, initial_time]  # [white_time_left, black_time_left]
        self.current_player = 0  # 0 for white, 1 for black
        self.last_move_time = time.time()

    def switch_player(self):
        self.current_player = 1 - self.current_player
        self.last_move_time = time.time()

    def get_time_left(self):
        elapsed_time = time.time() - self.last_move_time
        self.time_left[self.current_player] -= elapsed_time
        self.last_move_time = time.time()
        return self.time_left[self.current_player]

    def is_time_up(self):
        return self.get_time_left() < 0

class Player:
    def switch(turn):
        global current_player
        if current_player==1:
            current_player=0
        else:
            current_player=1
        
        return current_player
    
    def time_left(time):
        player1=time
        player2=time

        return('player 1 time: ', player1, 'player 2 time: ', player2)
    
    def find_histogram(clt):
        numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
        (hist, _) = np.histogram(clt.labels_, bins=numLabels)

        hist = hist.astype("float")
        hist /= hist.sum()

        return hist


# timer = ChessTimer(6)
# timer.switch_player()

print(Player.time_left(initial_time))

while(1):
    # Take each frame
    _, frame = cap.read()
    x, y, w, h = 50, 100, 200, 200
    x2, y2, w2, h2 =300, 100, 200, 200
    which_player=""

    #keeps looping 
    # left=timer.get_time_left()
    # print(left)

    #testing roi but cannot detect there specificaly 
    img=cv.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)
    img2=cv.rectangle(frame,(x2,y2),(x2+w2, y2+h2),(0,255,0),2)
    #cv.imshow('frame', img) 
    
    #print(frame.shape)
    img_roi=frame[y:y+h, x:x+w]
    img_roi2=frame[y2:y2+h2, x2:x2+h2]
    #print(img_roi.shape)
    #cv.imshow('roi', img_roi)
    hsv = cv.cvtColor(img_roi, cv.COLOR_BGR2HSV) # Convert BGR to HSV
    hsv2=cv.cvtColor(img_roi2, cv.COLOR_BGR2HSV)

    # for blue 
    lower_blue = np.array([94,80,2], np.uint8)  # define range of blue color in HSV
    upper_blue = np.array([120,255,255], np.uint8)
    blue_mask = cv.inRange(hsv, lower_blue, upper_blue) # Threshold HSV image for blue
    #blue_contours, _ =  cv.findContours(blue_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # for red 
    lower_red = np.array([94,80,2], np.uint8)  # define range of blue color in HSV
    upper_red = np.array([120,255,255], np.uint8)
    red_mask = cv.inRange(hsv2, lower_red, upper_red) 
    #red_contours, _ =  cv.findContours(red_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)


    kernal = np.ones((5, 5), "uint8")
    _,blue_thresh = cv.threshold(blue_mask,127,255,0)
    _,red_thresh = cv.threshold(red_mask,127,255,0)


    # Creating contour to track blue color
    blue_contours, hierarchy = cv.findContours(blue_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #cv.RETR_EXTERNAL
    #blue_contours = max(blue_contours, key=cv.contourArea)
    red_contours, hierarchy = cv.findContours(red_thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # if blue_contour in enumerate(blue_contours):
    #     print("detected left player")

    # if red_contour in enumerate(red_contours):
    #     print("detetected right player")

    for pic, blue_contour in enumerate(blue_contours): 
        which_player="left"
        for pic, red_contour in enumerate(red_contours):
                blue_area = cv.contourArea(blue_contour)
                red_area = cv.contourArea(red_contour)
                if(blue_area > 300 and red_area>300):
                    x, y, w, h = cv.boundingRect(blue_contour)
                    #imageFrame=cv.drawContours(frame, blue_contours, -1, (255, 0, 0), 3)
                    #imageFrame = cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    #cv.putText(imageFrame, "Blue Colour", (x, y), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))

                    x2,y2,w2,h2 = cv.boundingRect(red_contour)
                    #imageFrame2=cv.rectangle(frame,(x2,y2),(x2+w2, y2+h2),(0,255,0),2)
                    #cv.putText(imageFrame2, "Red", (x2, y2), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                    which_player="both"

        if which_player =="left":
            if had_both==True:
                # print("switch players")
                # need to make sure both is called before switching again
                # create a list to keep track of prior calls
                turn= Player.switch("left")
                had_both=False
                printed=False
                if turn==1:
                    print("player 1's turn")
                if turn==0:
                    print("player 2's turn")    

        if which_player=="both":
            if printed==False:
                print("Previous player in play")
                printed=True
            had_both=True

    #if (which_player=="both"):
         #for now example dec timer 1

    # printing out 
    cv.imshow('frame', frame)
    
    if cv.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv.destroyAllWindows()
        break
