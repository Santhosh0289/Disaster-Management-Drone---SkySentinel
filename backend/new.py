import cv2
import base64
import numpy as np

def capture_and_convert():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not access webcam")
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Failed to capture image")
        return

    # Convert image to Base64
    _, buffer = cv2.imencode(".jpg", frame)
    base64_str = base64.b64encode(buffer).decode("utf-8")

    # Create Data URL
    data_url = f"data:image/jpeg;base64,{base64_str}"
    print("Base64 Image URL:", data_url)

    return data_url

capture_and_convert()
