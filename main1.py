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

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiple Wobbling Bouncing Images")

# Example image files (put your filenames here)
image_files = ["images\microbe-1.png", "images\microbe-2.png", "images\microbe-3.png"]  # Replace with your actual image paths

# Load images and initialize object data
sprites = []
for img_file in image_files:
    img = pygame.image.load(img_file).convert_alpha()
    base_size = 80
    img = pygame.transform.smoothscale(img, (base_size, base_size))
    
    sprite = {
        "image": img,
        "original": img,  # Keep unmodified for future scaling/rotation
        "rect": img.get_rect(
            center=(random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 100))
        ),
        "speed": [random.choice([-2, 2]), random.choice([-1, 1])],
        "time": random.uniform(0, 10),  # unique phase offset
    }
    sprites.append(sprite)

# Clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000.0  # seconds since last frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if cap.isOpened() == False:
        running = False

    screen.fill((0, 0, 0))

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

    for sprite in sprites:
        # if no bodies are found
        if results.pose_landmarks == None:
            sprite["time"] += dt

            # Move
            sprite["rect"].x += sprite["speed"][0]
            sprite["rect"].y += sprite["speed"][1]

            # Bounce
            if sprite["rect"].left < 0 - 150 or sprite["rect"].right > WIDTH + 150:
                sprite["speed"][0] *= -1
            if sprite["rect"].top < 0 - 150 or sprite["rect"].bottom > HEIGHT + 150:
                sprite["speed"][1] *= -1

            # Wobble: small rotation over time
            angle = 10 * math.sin(sprite["time"] * 4)  # 10° back and forth

            # Optional: scale size for pulsing effect
            scale_factor = 1 + 0.1 * math.sin(sprite["time"] * 5)
            new_size = (
                int(sprite["original"].get_width() * scale_factor),
                int(sprite["original"].get_height() * scale_factor)
            )
            transformed = pygame.transform.rotozoom(sprite["original"], angle, scale_factor)

        elif results.post_landmarks != None:
            x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_THUMB].x * frame.shape[1])
            y = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_THUMB].y * frame.shape[0])

        
        # Update rect to keep center consistent
        sprite_rect = transformed.get_rect(center=sprite["rect"].center)
        screen.blit(transformed, sprite_rect)

    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
pygame.quit()
sys.exit()