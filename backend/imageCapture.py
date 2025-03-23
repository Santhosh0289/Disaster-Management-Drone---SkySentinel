from djitellopy import tello
import cv2
import os
from datetime import datetime

# Initialize drone
drone = tello.Tello()
drone.connect()
drone.streamon()

print(f"Battery: {drone.get_battery()}%")

# Create folder for saving images
save_dir = "images"
os.makedirs(save_dir, exist_ok=True)

while True:
    frame = drone.get_frame_read().frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

    # Resize for display
    resized_frame = cv2.resize(frame, (360, 240))

    # Display the image
    cv2.imshow("Drone Camera", resized_frame)

    # Wait for key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # Capture image when 'C' is pressed
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(save_dir, f"{timestamp}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Captured: {filename}")

    elif key == ord('q'):  # Quit when 'Q' is pressed
        print("Exiting...")
        break

# Clean up
cv2.destroyAllWindows()
drone.streamoff()
