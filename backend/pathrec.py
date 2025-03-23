import json
import time
from djitellopy import Tello

# Initialize drone
drone = Tello()
drone.connect()
drone.streamon()

print(f"Battery: {drone.get_battery()}%")

# Dictionary to store paths
try:
    with open("paths.json", "r") as f:
        paths = json.load(f)  # Load existing paths
except FileNotFoundError:
    paths = {}

path_name = input("Enter a name for this path (e.g., path1): ")

# Ensure unique path name
if path_name in paths:
    print(f"Path '{path_name}' already exists! Choose a different name.")
    exit()

commands = []  # Store (command, distance)
drone.takeoff()
start_time = time.time()

try:
    while True:
        print("\nCommands: [ w: forward | s: backward | a: left | d: right | u: up | j: down | q: rotate left | e: rotate right | x: stop & save ]")
        cmd = input("Enter command: ").strip().lower()

        if cmd == "x":  # Stop recording
            break

        speed = 30  # cm/s
        duration = float(input("Duration (seconds): "))
        distance = int(speed * duration)  # Convert time to distance (cm)

        if cmd in ["w", "s", "a", "d", "u", "j", "q", "e"]:
            commands.append((cmd, distance))  # Store command and distance
        
        # Use precise movement functions
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
            drone.rotate_counter_clockwise(distance)  # Rotations need degrees
        elif cmd == "e":
            drone.rotate_clockwise(distance)

except KeyboardInterrupt:
    print("\nRecording stopped.")

drone.land()
paths[path_name] = commands  # Save path
with open("paths.json", "w") as f:
    json.dump(paths, f, indent=4)

print(f"Path '{path_name}' saved successfully!")

