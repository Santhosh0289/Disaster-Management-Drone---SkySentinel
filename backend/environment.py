import json
import time
import cv2
import os
import torch
import numpy as np
from datetime import datetime
from djitellopy import Tello
import threading
from ultralytics import YOLO

model = YOLO("yolov8n.pt") 

# Initialize drone
drone = Tello()
drone.connect()
drone.streamon()

print(f"Battery: {drone.get_battery()}%")

# Load saved paths
try:
    with open("paths.json", "r") as f:
        paths = json.load(f)
except FileNotFoundError:
    print("No saved paths found!")
    exit()

print("\nAvailable Paths:", ", ".join(paths.keys()))
path_name = input("Enter the path to replay: ").strip()

if path_name not in paths:
    print("Invalid path name!")
    exit()

commands = paths[path_name]

# Debug: Check the order of loaded commands
print(f"Loaded commands for {path_name}: {commands}")

# Create directory structure for storing images
base_dir = "images"
path_dir = os.path.join(base_dir, path_name)
date_dir = os.path.join(path_dir, datetime.now().strftime("%Y-%m-%d"))
os.makedirs(date_dir, exist_ok=True)

# Flag to control the photo capture thread
capturing = True

# Function to detect objects using YOLO
def detect_objects(frame):
    results = model(frame)[0]  # Run YOLO detection
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = result
        label = model.names[int(cls)]
        
        if label in ["person", "fire", "smoke"]:  # Adjust based on the dataset labels
            color = (0, 255, 0) if label == "person" else (0, 0, 255)  # Green for people, Red for fire
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame

def capture_photos():
    while capturing:
        frame = drone.get_frame_read().frame
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            frame = cv2.resize(frame, (600, 600))  # Resize for display

            # Detect objects
            frame = detect_objects(frame)

            cv2.imshow("Live Feed", frame)  # Show live feed with detections
            cv2.waitKey(1)  # Required to update OpenCV window
            
            # Save image
            timestamp = datetime.now().strftime("%H-%M-%S-%f")[:-3]  # Include milliseconds
            filename = os.path.join(date_dir, f"{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captured: {filename}")
        
        time.sleep(2)  # Capture every 2 seconds


# Start taking photos before takeoff
photo_thread = threading.Thread(target=capture_photos)
photo_thread.start()

print(f"Replaying path: {path_name}")
drone.takeoff()

try:
    for cmd, distance in commands:
        print(f"Executing: {cmd} for {distance} cm")  # Debugging

        if cmd == "w":
            drone.move_forward(distance)
        elif cmd == "s":
            drone.move_back(distance)
        elif cmd == "a":
            drone.move_left(distance)
        elif cmd == "d":
            drone.move_right(distance)
        elif cmd == "u":
            drone.move_up(distance)
        elif cmd == "j":
            drone.move_down(distance)
        elif cmd == "q":
            drone.rotate_counter_clockwise(distance)  # Rotations use degrees
        elif cmd == "e":
            drone.rotate_clockwise(distance)

        time.sleep(1)  # Ensure stability before next movement

except KeyboardInterrupt:
    print("\nReplay interrupted.")

# Stop the photo capture thread and land the drone
capturing = False
photo_thread.join()
drone.land()
print("Path replay complete!")