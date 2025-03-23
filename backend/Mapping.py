import pygame
import numpy as np
import cv2
import math
import folium
import geocoder
import webbrowser
import time
from djitellopy import tello

# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.iconify()  # Hide pygame window

# Drone Initialization
drone = tello.Tello()
drone.connect()
drone.streamon()
print(f"Drone Battery: {drone.get_battery()}%")

# Scaling & Flight Constants
scale_factor = 10  # Pixels to feet conversion
speed = 30  # Drone speed (cm/s)
interval = 0.25  # Time step
dInterval = (speed / 30.48) * interval * scale_factor
aInterval = 60 * interval  # Rotation speed

# Initial Position & Orientation
x, y = 500, 500
yaw = 0
points = [(x, y)]

# Fetch Initial GPS Position
def get_live_location():
    """Fetch approximate real-time latitude & longitude."""
    g = geocoder.ip("me")
    return [17.5449, 78.5718]  # Default to BITS Pilani Hyderabad

# Update Map with Flight Path
def update_map():
    """Generate and update the real-time drone flight path map."""
    lat, lon = get_live_location()
    live_map = folium.Map(location=[lat, lon], zoom_start=19)

    for idx, (px, py) in enumerate(points):
        point_lat = lat + (py - 500) / 100000
        point_lon = lon + (px - 500) / 100000
        folium.CircleMarker([point_lat, point_lon], radius=3, color="red").add_to(live_map)

    folium.Marker([lat, lon], popup="Drone", icon=folium.Icon(color="blue")).add_to(live_map)
    live_map.save("map.html")
    webbrowser.open("map.html")

# Get Keyboard Inputs
def getKeyBoardInput():
    """Reads keyboard inputs and updates drone movement & yaw angle."""
    global x, y, yaw
    lr, fb, ud, yv = 0, 0, 0, 0

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]: lr = -speed
    elif keys[pygame.K_RIGHT]: lr = speed

    if keys[pygame.K_UP]: fb = speed
    elif keys[pygame.K_DOWN]: fb = -speed

    if keys[pygame.K_w]: ud = speed
    elif keys[pygame.K_s]: ud = -speed

    if keys[pygame.K_a]: yv = -60
    elif keys[pygame.K_d]: yv = 60

    if keys[pygame.K_q]: drone.land()
    if keys[pygame.K_e]: drone.takeoff()

    if keys[pygame.K_m]: update_map()  # Update map when 'M' is pressed

    # Send movement commands to drone
    drone.send_rc_control(lr, fb, ud, yv)

    # Update position & yaw
    yaw += yv * interval
    x += int(fb * math.cos(math.radians(yaw)) - lr * math.sin(math.radians(yaw)))
    y += int(fb * math.sin(math.radians(yaw)) + lr * math.cos(math.radians(yaw)))

    return [x, y]

# Draw Flight Path
def drawPoints(img, points):
    """Draws the flight path and current position."""
    for point in points:
        cv2.circle(img, point, 3, (0, 0, 255), cv2.FILLED)
    
    cv2.circle(img, points[-1], 6, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0]-500)/scale_factor:.2f}, {(500 - points[-1][1])/scale_factor:.2f}) ft',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

# Main Loop
while True:
    x, y = getKeyBoardInput()

    img = np.zeros((1000, 1000, 3), np.uint8)
    for i in range(0, 1000, 100):
        cv2.line(img, (i, 0), (i, 1000), (50, 50, 50), 1)
        cv2.line(img, (0, i), (1000, i), (50, 50, 50), 1)

    if points[-1] != (x, y):
        points.append((x, y))

    drawPoints(img, points)
    cv2.imshow('Drone Flight Path', img)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cv2.destroyAllWindows()
            exit()
    
    cv2.waitKey(1)
