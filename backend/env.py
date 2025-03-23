import cv2
from djitellopy import Tello
from ultralytics import YOLO
import numpy as np
import requests
import tkinter as tk
from tkinter import messagebox

# Initialize DJI Tello
tello = Tello()
tello.connect()
tello.streamon()

# Load AI Model for Smoke/Fire Detection
model = YOLO("yolov8n.pt")

def detect_smoke_fire(frame):
    results = model(frame)
    
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            conf = float(box.conf[0])  
            label = r.names[int(box.cls[0])]

            if label in ["smoke", "fire"] and conf > 0.4:
                color = (0, 0, 255) if label == "fire" else (255, 255, 0)  
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label.upper()} ({conf:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
               

    return frame

def detect_fog(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

    if laplacian < 50:
        cv2.putText(frame, "🚨 Fog/Haze Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        

    return frame

def air_quality_index(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dark_pixels = np.sum(gray < 100)  
    total_pixels = frame.shape[0] * frame.shape[1]
    haze_index = (dark_pixels / total_pixels) * 100

    if haze_index > 40:
        cv2.putText(frame, f"⚠ Poor Air Quality: HI={haze_index:.2f}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
     

    return frame


def show_alert(message):
    # Create a hidden root window
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Show the popup alert
    messagebox.showwarning("🚨 Drone Alert", message)
    
    # Destroy the window after closing the alert
    root.destroy()

# Example Usage: Trigger an alert for smoke detection
if __name__ == "__  main__":
    show_alert("🚨 Smoke detected by the drone! Take action immediately.")

while True:
    frame = tello.get_frame_read().frame
    frame = cv2.resize(frame, (640, 480))

    # Apply AI Detection
    frame = detect_smoke_fire(frame)
    frame = detect_fog(frame)
    frame = air_quality_index(frame)

    # Display live video
    cv2.imshow("Drone Environmental Monitoring", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
tello.streamoff()