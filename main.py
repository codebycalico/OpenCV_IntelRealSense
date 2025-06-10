# Creating a draft for the microbe "game"
# that tracks pedestrians and microbes stick
# as they pass
# Calico Rose Randall

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

# create capture object
cap = cv2.VideoCapture(0)

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Images Follow Mouse While Button Held")

# === CONFIG ===
image_files = ["images/microbe-1.png", "images/microbe-2.png", "images/microbe-3.png"]  # Replace with your image file paths
base_size = 80
float_amplitude = 5
move_speed = 3

# === LOAD IMAGES & CREATE SPRITES ===
sprites = []
for img_file in image_files:
    original_image = pygame.image.load(img_file).convert_alpha()
    scaled_image = pygame.transform.smoothscale(original_image, (base_size, base_size))
    rect = scaled_image.get_rect(
        topleft=(random.randint(0, WIDTH - base_size), random.randint(0, HEIGHT - base_size))
    )
    
    sprite = {
        "image": scaled_image,
        "original": scaled_image,
        "rect": rect,
        "pos": [float(rect.x), float(rect.y)],
        "speed": [random.choice([-3, 3]), random.choice([-3, 3])],
        "float_time": random.uniform(0, 10)
    }
    sprites.append(sprite)

clock = pygame.time.Clock()
mouse_held = False

# === MAIN LOOP ===
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    screen.fill((0, 0, 0))

    for sprite in sprites:
        pos_x, pos_y = sprite["pos"]
        speed_x, speed_y = sprite["speed"]
        sprite["float_time"] += dt

        if results.pose_landmarks != None:
            ped_x = int(results.pose_landmarks.landmark[0].x * frame.shape[1])
            ped_y = int(results.pose_landmarks.landmark[0].y * frame.shape[0])
            # Move smoothly toward the mouse
            target_x, target_y = ped_x, ped_y
            dir_x = target_x - pos_x
            dir_y = target_y - pos_y
            dist = math.hypot(dir_x, dir_y)

            if dist != 0:
                dir_x /= dist
                dir_y /= dist
                move_x = dir_x * min(move_speed, dist)
                move_y = dir_y * min(move_speed, dist)
                pos_x += move_x
                pos_y += move_y
        else:
            # Bounce and float
            float_offset = float_amplitude * math.sin(sprite["float_time"] * 3)

            pos_x += speed_x
            pos_y += speed_y

            # Bounce off edges
            if pos_x < 0 or pos_x + base_size > WIDTH:
                sprite["speed"][0] *= -1
            if pos_y + float_offset < 0 or pos_y + base_size + float_offset > HEIGHT:
                sprite["speed"][1] *= -1

            pos_y += float_offset

        # Update sprite position and draw
        sprite["pos"] = [pos_x, pos_y]
        sprite["rect"].topleft = (int(pos_x), int(pos_y))
        screen.blit(sprite["image"], sprite["rect"])

    pygame.display.flip()

pygame.quit()
sys.exit()