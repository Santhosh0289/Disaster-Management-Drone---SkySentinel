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

# Flag to indicate manual control mode
manual_control = False

# Temporary path recording
temporary_path = []
start_position = None

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
    global start_position
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
    
    # Return to the start position of the circle
    print("Returning to the start position of the circle...")
    drone.go_xyz_speed(-x, -y, 0, CIRCLE_SPEED)
    time.sleep(1)
    
    print("360-degree photo capture complete!")

def manual_control_mode():
    global manual_control, temporary_path
    print("Entering manual control mode. Use WASD to control the drone. Press 'c' to confirm position.")
    
    while manual_control:
        key = cv2.waitKey(1) & 0xFF
        
        # Manual controls
        if key == ord('w'):  # Move forward
            drone.move_forward(50)
            temporary_path.append(("w", 50))
        elif key == ord('s'):  # Move backward
            drone.move_back(50)
            temporary_path.append(("s", 50))
        elif key == ord('a'):  # Move left
            drone.move_left(50)
            temporary_path.append(("a", 50))
        elif key == ord('d'):  # Move right
            drone.move_right(50)
            temporary_path.append(("d", 50))
        elif key == ord('u'):  # Move up
            drone.move_up(50)
            temporary_path.append(("u", 50))
        elif key == ord('j'):  # Move down
            drone.move_down(50)
            temporary_path.append(("j", 50))
        elif key == ord('q'):  # Rotate counter-clockwise
            drone.rotate_counter_clockwise(45)
            temporary_path.append(("q", 45))
        elif key == ord('e'):  # Rotate clockwise
            drone.rotate_clockwise(45)
            temporary_path.append(("e", 45))
        elif key == ord('c'):  # Confirm position
            print("Position confirmed. Exiting manual control mode.")
            manual_control = False
            break

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

        # Check for manual control mode
        key = cv2.waitKey(1) & 0xFF
        if key == ord('d'):  # Press 'd' to enter manual control mode
            print("Switching to manual control mode...")
            manual_control = True
            start_position = (drone.get_current_state().get("x", 0), drone.get_current_state().get("y", 0))
            temporary_path = []  # Reset temporary path
            manual_control_mode()

            # After confirming position, circle the object
            circle_object()

            # Return to the start position of the circle
            print("Returning to the start position of the circle...")
            drone.go_xyz_speed(-start_position[0], -start_position[1], 0, CIRCLE_SPEED)
            time.sleep(1)

            # Replay the temporary path to resume the original path
            print("Resuming replay path...")
            for temp_cmd, temp_dist in temporary_path:
                if temp_cmd == "w":
                    drone.move_forward(temp_dist)
                elif temp_cmd == "s":
                    drone.move_back(temp_dist)
                elif temp_cmd == "a":
                    drone.move_left(temp_dist)
                elif temp_cmd == "d":
                    drone.move_right(temp_dist)
                elif temp_cmd == "u":
                    drone.move_up(temp_dist)
                elif temp_cmd == "j":
                    drone.move_down(temp_dist)
                elif temp_cmd == "q":
                    drone.rotate_counter_clockwise(temp_dist)
                elif temp_cmd == "e":
                    drone.rotate_clockwise(temp_dist)
                time.sleep(1)

except KeyboardInterrupt:
    print("\nReplay interrupted.")

# Stop the photo capture thread and land the drone
capturing = False
photo_thread.join()
drone.land()
print("Path replay complete!")