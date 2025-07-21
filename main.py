# Creating a draft for the microbe "game"
# that tracks pedestrians and microbes stick
# as they pass
# Calico Rose Randall
# Human Pose Estimation with OpenCV
# https://techvidvan.com/tutorials/human-pose-estimation-opencv/
# https://github.com/verma-ananya/HumanBody-Skeleton-Detection-using-OpenCV
# Pose landmark detection guide
# https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker

import pygame
import sys
import math
import random
import cv2
import mediapipe as mp

# initialize Pose estimator / detector
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# create capture object (video feed)
cap = cv2.VideoCapture(0)

# initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Microbes Float And Follow Body When Detected")

# Image / Sprite configuration
# If problem with images loading, check the file path for the images
image_files = ["images/microbe-1.png", "images/microbe-2.png", "images/microbe-3.png"]
base_size = 100
move_speed = 3
# how much random movement to add
jitter_strength = 3

# Load images and create array of sprites from images
sprites = []
# loop through images loaded into array and set them up as sprites
for img_file in image_files:
    original_image = pygame.image.load(img_file).convert_alpha()
    # scale down the size
    scaled_image = pygame.transform.smoothscale(original_image, (base_size, base_size))
    # rect is the position that the sprite is on the screen at any given time
    # topleft is the starting position
    rect = original_image.get_rect(
        topleft=(random.randint(0, WIDTH - base_size), random.randint(0, HEIGHT - base_size))
    )
    
    # sprite class
    sprite = {
        "image": scaled_image,
        "rect": rect,
        "pos": [float(rect.x), float(rect.y)],
        "speed": [random.choice([-3, 3]), random.choice([-3, 3])]
    }
    sprites.append(sprite)

# main loop 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # read frame from capture object
    _, frame = cap.read()

    # convert the frame to RGB format & flip horizaontally
    RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 0)

    # process the RGB frame to get the result
    results = pose.process(RGB)

    # draw detected skeleton on the frame
    mp_drawing.draw_landmarks(
        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    #continuously draw a black background
    screen.fill((0, 0, 0))

    # loop through each sprite to move it around the screen
    for sprite in sprites:
        pos_x, pos_y = sprite["pos"]
        speed_x, speed_y = sprite["speed"]

        # if we have detected a body
        if results.pose_landmarks != None:
            body_x = int(results.pose_landmarks.landmark[0].x * frame.shape[1])
            body_y = int(results.pose_landmarks.landmark[0].y * frame.shape[0])
            # Move smoothly toward the tracked person
            dir_x = body_x - pos_x
            dir_y = body_y - pos_y
            dist = math.hypot(dir_x, dir_y)

            if dist != 0:
                dir_x /= dist
                dir_y /= dist
                pos_x += dir_x * move_speed
                pos_y += dir_y * move_speed

        #if we haven't detected a body
        else:
             # Move around and add random jitter to movement
            jitter_x = random.uniform(-jitter_strength, jitter_strength)
            jitter_y = random.uniform(-jitter_strength, jitter_strength)

            pos_x += speed_x + jitter_x
            pos_y += speed_y + jitter_y

            # Turn around and come back on screen if they go off screen
            if pos_x < -150 or pos_x + base_size > (WIDTH + 150):
                sprite["speed"][0] *= -1
            if pos_y < -150 or pos_y + base_size > (HEIGHT + 150):
                sprite["speed"][1] *= -1

        # Update sprite position and draw
        sprite["pos"] = [pos_x, pos_y]
        sprite["rect"].topleft = (int(pos_x), int(pos_y))
        # move the image to the new location
        screen.blit(sprite["image"], sprite["rect"])

    # shows everything, essentially like FastLED.show()
    # prevents flickering as it loads everything
    # and then shows it all at once
    pygame.display.flip()

pygame.quit()
sys.exit()