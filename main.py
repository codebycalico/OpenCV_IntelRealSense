# ----------------------------- Include files
import mediapipe as mp
import cv2 as cv
import numpy as np
import math
import time
import handModule as hm
import pyrealsense2 as rs

## Declare stuff
cap = cv.VideoCapture(0)

detector = hm.HandDetector(detectionCon = 0.75, trackCon = 0.6)

pipeline = rs.pipeline()
pipeline.start()

while cap.isOpened():
    # create a pipeline object. this object configures the camers & owns its handle
    frames = pipeline.wait_for_frames()
    depth = frames.get_depth_frame()
    success, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # You can change the display window size by resizing frame here.

    img = detector.findHands(frame) # Draws hands onto img

    detector.findPosition(frame, 2)
    #detector.fingerCount(frame, 2)

    #grabbed = detector.checkGrabAlt(frame, 2)
    #print(grabbed)
    
    # returns the coordinates of the center
    # works on two hands at the same time, creating two lists of x, y coordinates
    center = detector.center_of_mass(frame)
    print(center)
    for hand in center:
        print(depth.get_distance(hand[0], hand[1]))

    # do stuff:
    # If you want to draw stuff or add text, draw it onto img, not frame.


    cv.imshow('Video', frame)         # Display img.

    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()