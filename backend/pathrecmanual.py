import json
import keypress as kp
from djitellopy import Tello
from time import sleep

# Initialize keyboard controls
kp.init()

# Initialize drone
drone = Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")

# Load existing paths
try:
    with open("paths.json", "r") as f:
        paths = json.load(f)
except FileNotFoundError:
    paths = {}

path_name = input("Enter a name for this path (e.g., path1): ")

# Ensure unique path name
if path_name in paths:
    print(f"Path '{path_name}' already exists! Choose a different name.")
    exit()

commands = []  # Store movement commands

def getKeyBoardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50  # Speed value

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yv = -speed
    elif kp.getKey("d"): yv = speed

    if kp.getKey("q"):  # Land and exit
        print("\nLanding drone...")
        drone.land()
        save_path()
        exit()

    if kp.getKey("e"):  # Takeoff
        print("Taking off...")
        drone.takeoff()

    if kp.getKey("x"):  # Stop recording and land
        print("\nStopping recording...")
        drone.land()
        save_path()
        exit()

    return [lr, fb, ud, yv]

def save_path():
    """Save recorded movements to JSON."""
    paths[path_name] = commands
    with open("paths.json", "w") as f:
        json.dump(paths, f, indent=4)
    print(f"✅ Path '{path_name}' saved successfully!")

print("\nUse arrow keys for movement, 'WASD' for altitude/rotation.")
print("Press 'E' to Takeoff | 'Q' to Land | 'X' to Stop & Save.")

# Control loop
try:
    while True:
        vals = getKeyBoardInput()
        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        
        # Record movement if any input is detected
        if any(vals):
            commands.append(vals)
        
        sleep(0.05)  # Control update frequency

except KeyboardInterrupt:
    print("\nEmergency Stop Detected! Landing Drone...")
    drone.land()
    save_path()
