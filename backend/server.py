from fastapi import FastAPI
from djitellopy import Tello
import json
import threading
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import cv2
from fastapi.responses import StreamingResponse
import time

# Add CORS middleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

drone = Tello()

# Connect to the drone
drone.connect()
drone.streamon()
print(f"Battery: {drone.get_battery()}%")

# Load saved paths
try:
    with open("paths.json", "r") as f:
        paths = json.load(f)
except FileNotFoundError:
    paths = {}

# Keep-alive thread
keep_alive_thread = None
keep_alive_running = False

def keep_alive():
    while keep_alive_running:
        drone.send_control_command("command")  # Send a keep-alive command
        time.sleep(10)  # Send every 10 seconds

# Command model
class Command(BaseModel):
    path_name: str
    commands: list  # List of {cmd, duration}

# Takeoff endpoint
@app.post("/takeoff/")
def takeoff():
    global keep_alive_thread, keep_alive_running

    # Start keep-alive thread
    keep_alive_running = True
    keep_alive_thread = threading.Thread(target=keep_alive)
    keep_alive_thread.start()

    drone.takeoff()
    return {"message": "✅ Drone took off! Please enter commands."}

# Landing endpoint
@app.post("/land/")
def land():
    global keep_alive_running

    # Stop keep-alive thread
    keep_alive_running = False
    if keep_alive_thread:
        keep_alive_thread.join()

    drone.land()
    return {"message": "🛬 Drone landed safely!"}

# Execute commands
def execute_commands(path_name, commands):
    for command in commands:
        cmd = command["cmd"]
        duration = command["duration"]
        speed = 30  # cm/s
        distance = int(speed * duration)

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
            drone.rotate_counter_clockwise(distance * 10)
        elif cmd == "e":
            drone.rotate_clockwise(distance * 10)

    paths[path_name] = commands
    with open("paths.json", "w") as f:
        json.dump(paths, f, indent=4)

    print(f"Path '{path_name}' executed and saved successfully!")

# API to start command execution after takeoff
@app.post("/execute-commands/")
def execute_commands_api(data: Command):
    path_name = data.path_name
    commands = data.commands

    if not commands:
        return {"error": "❌ No commands provided!"}

    # Run command execution in a separate thread
    thread = threading.Thread(target=execute_commands, args=(path_name, commands))
    thread.start()

    return {"message": f"🚀 Executing commands for {path_name}..."}

# Video feed endpoint
# Video feed endpoint
@app.get("/video_feed")
def video_feed():
    def generate():
        frame_reader = drone.get_frame_read()
        while True:
            frame = frame_reader.frame
            if frame is None:
                continue  # Skip if the frame is not available

            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

# Get saved paths
@app.get("/paths")
def get_saved_paths():
    return paths

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

