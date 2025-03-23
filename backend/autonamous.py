import time
import cv2
import numpy as np
from djitellopy import Tello
from simple_pid import PID

# Initialize Tello
tello = Tello()
tello.connect()
tello.streamon()  # Start live video feed

# PID Controller for Forward Motion
pid_forward = PID(0.4, 0.01, 0.05, setpoint=150)  # Tweak values as needed
pid_forward.output_limits = (-30, 30)

def detect_obstacle(frame):
    """Detect obstacles using edge detection (Canny)."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    edges = cv2.Canny(gray, 100, 200)  # Detect edges
    
    # Count white pixels (edges) in center area
    height, width = edges.shape
    center_region = edges[height//3 : 2*height//3, width//4 : 3*width//4]
    
    obstacle_pixels = np.sum(center_region == 255)
    
    return obstacle_pixels > 500  # If too many edges, consider it an obstacle

def autonomous_flight():
    tello.takeoff()
    time.sleep(2)

    while True:
        frame = tello.get_frame_read().frame
        frame = cv2.resize(frame, (400, 300))
        
        # Detect obstacles
        obstacle_detected = detect_obstacle(frame)

        if obstacle_detected:
            print("🚧 Obstacle detected! Stopping or turning...")
            tello.send_rc_control(0, 0, 0, 20)  # Rotate to avoid obstacle
            time.sleep(0.5)
        else:
            print("✅ Path is clear. Moving forward...")
            tello.send_rc_control(0, 20, 0, 0)  # Move forward

        cv2.imshow("Tello Live Feed", frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    tello.land()
    cv2.destroyAllWindows()

# Run autonomous flight
autonomous_flight()