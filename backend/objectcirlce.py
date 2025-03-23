import json
import time
import cv2
import os
from datetime import datetime
from djitellopy import Tello
import threading
import math

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

# Flag to indicate if an object has been detected
object_detected = False

# Circle parameters
CIRCLE_RADIUS = 100  # Radius in cm
CIRCLE_SPEED = 20  # Speed in cm/s
PHOTO_INTERVAL = 45  # Degrees between photos

def capture_photos():
    while capturing:
        frame = drone.get_frame_read().frame
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            frame = cv2.resize(frame, (600, 600))  # Resize for display
            cv2.imshow("Live Feed", frame)  # Show live feed
            cv2.waitKey(1)  # Required to update OpenCV window
            
            # Save image
            timestamp = datetime.now().strftime("%H-%M-%S-%f")[:-3]  # Include milliseconds
            filename = os.path.join(date_dir, f"{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captured: {filename}")
        
        time.sleep(2)  # Capture every 2 seconds

def circle_object():
    global object_detected
    print("Starting to circle the object...")
    
    # Calculate the circumference and time to complete a full circle
    circumference = 2 * math.pi * CIRCLE_RADIUS
    total_time = circumference / CIRCLE_SPEED
    
    # Calculate the number of photos to take
    num_photos = 360 // PHOTO_INTERVAL
    
    # Start circling
    for i in range(num_photos):
        # Move in a circular path
        angle = i * PHOTO_INTERVAL
        x = int(CIRCLE_RADIUS * math.cos(math.radians(angle)))
        y = int(CIRCLE_RADIUS * math.sin(math.radians(angle)))
        
        # Move the drone to the new position
        drone.go_xyz_speed(x, y, 0, CIRCLE_SPEED)
        time.sleep(1)  # Wait for the drone to stabilize
        
        # Capture a photo
        frame = drone.get_frame_read().frame
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            timestamp = datetime.now().strftime("%H-%M-%S-%f")[:-3]
            filename = os.path.join(date_dir, f"circle_{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captured 360-degree photo: {filename}")
    
    print("360-degree photo capture complete!")
    object_detected = False

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

        # Check for manual object detection
        if not object_detected:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('d'):  # Press 'd' to detect an object
                print("Object detected manually! Starting 360-degree photo capture...")
                object_detected = True
                circle_object()

except KeyboardInterrupt:
    print("\nReplay interrupted.")

# Stop the photo capture thread and land the drone
capturing = False
photo_thread.join()
drone.land()
print("Path replay complete!")