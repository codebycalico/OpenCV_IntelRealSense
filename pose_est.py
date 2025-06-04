# TechVidvan Human pose estimator
# https://techvidvan.com/tutorials/human-pose-estimation-opencv/
# Adapted by Calico Randall

import cv2
import mediapipe as mp

# initialize Pose estimator / detector
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# create capture object
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # read frame from capture object
    _, frame = cap.read()

    # convert the frame to RGB format
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # process the RGB frame to get the result
    results = pose.process(RGB)

    #print(results.pose_landmarks)

    # draw detected skeleton on the frame
    mp_drawing.draw_landmarks(
        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
    # find the x, y coordinates for whatever specific landmark you want to track
    if results.pose_landmarks != None:
        print("Right Thumb:")
        x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_THUMB].x * frame.shape[1])
        y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_THUMB].y * frame.shape[0])
        print(x,y)

    # show the final output
    cv2.imshow('Output', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
