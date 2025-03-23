import json
import time
import os
import threading
import cv2
import torch
import numpy as np
from datetime import datetime
from fastapi import FastAPI, WebSocket, BackgroundTasks, WebSocketDisconnect
from djitellopy import Tello
from ultralytics import YOLO
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model for object detection
model = YOLO("yolov8n.pt")

# Initialize the drone
drone = Tello()
drone.connect()
drone.streamon()
time.sleep(2)  # Wait for the camera to start
print(f"Battery: {drone.get_battery()}%")

# Load saved paths
paths_file = "paths.json"
if os.path.exists(paths_file):
    with open(paths_file, "r") as f:
        paths = json.load(f)
else:
    paths = {}

# Store flight state
capturing = False
photo_thread = None

# Directory for saving images
base_dir = "images"

# Function to detect objects using YOLO
def detect_objects(frame):
    results = model(frame)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = result
        label = model.names[int(cls)]
        color = (0, 255, 0)  # Green for all objects
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return frame

# Function to capture photos in a separate thread
def capture_photos(path_name):
    global capturing
    capturing = True
    path_dir = os.path.join(base_dir, path_name)
    date_dir = os.path.join(path_dir, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(date_dir, exist_ok=True)
    
    while capturing:
        frame = drone.get_frame_read().frame
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (600, 600))
            frame = detect_objects(frame)
            timestamp = datetime.now().strftime("%H-%M-%S-%f")[:-3]
            filename = os.path.join(date_dir, f"{timestamp}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Captured: {filename}")
        else:
            print("No frame received from drone camera!")
        time.sleep(2)  # Capture every 2 seconds

# API Endpoint: Get available flight paths
@app.get("/paths")
async def get_paths():
    return {"available_paths": list(paths.keys())}

# API Endpoint: Start replaying a saved flight path
@app.post("/start/{path_name}")
async def start_flight(path_name: str):
    global photo_thread
    if path_name not in paths:
        return {"error": "Invalid path name!"}
    
    commands = paths[path_name]
    photo_thread = threading.Thread(target=capture_photos, args=(path_name,))
    photo_thread.start()
    drone.takeoff()
    
    try:
        for cmd, distance in commands:
            print(f"Executing: {cmd} for {distance} cm")
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
                drone.rotate_counter_clockwise(distance)
            elif cmd == "e":
                drone.rotate_clockwise(distance)
            time.sleep(1)
    except Exception as e:
        return {"error": str(e)}
    return {"message": f"Flight path {path_name} started"}

# API Endpoint: Stop flight and land the drone
@app.post("/stop")
async def stop_flight():
    global capturing
    capturing = False
    if photo_thread:
        photo_thread.join()
    drone.land()
    return {"message": "Drone landed successfully"}

# WebSocket Endpoint: Stream live video with object detection
@app.websocket("/video")
async def video_stream(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection established")
    
    while True:
        try:
            frame = drone.get_frame_read().frame
            if frame is None:
                print("No frame received from drone camera!")
                await websocket.send_text("No frame available")
                time.sleep(0.2)
                continue
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (600, 600))
            frame = detect_objects(frame)
            _, buffer = cv2.imencode(".jpg", frame)
            if buffer is None:
                print("Failed to encode frame")
                continue
            await websocket.send_bytes(buffer.tobytes())
            print("Frame sent successfully")
        except WebSocketDisconnect:
            print("WebSocket disconnected")
            break
        except Exception as e:
            print(f"WebSocket error: {e}")
            break
        time.sleep(0.1)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
