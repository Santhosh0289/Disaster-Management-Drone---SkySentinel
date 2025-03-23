import json
import time
import cv2
import os
from datetime import datetime
from djitellopy import Tello
import threading

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

def emergency_landing():
    input("\nPress Enter at any time to perform an emergency landing...")
    drone.emergency()
    print("Emergency landing activated!")
    exit()

# Start emergency landing listener
emergency_thread = threading.Thread(target=emergency_landing, daemon=True)
emergency_thread.start()

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

# Land the drone
drone.land()
print("Path replay complete!")
