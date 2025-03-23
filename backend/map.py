import pygame
import numpy as np
import cv2
import math
import folium
import geocoder
import webbrowser
from time import sleep

# Initialize pygame only once
pygame.init()
screen = pygame.display.set_mode((100, 100))  # Small hidden window for key events
pygame.display.iconify()  # Hide pygame window

# Scaling factor: 1000x1000 pixels (OpenCV) = 100x100 ft (Real)
scale_factor = 10  # 10 pixels = 1 ft

# Flight Parameters
fSpeed = 30  # Forward speed (cm/s)
aSpeed = 60  # Angular speed (deg/s)
interval = 0.25  # Time step

dInterval = (fSpeed / 30.48) * interval * scale_factor  # Convert cm to ft, then to pixels
aInterval = aSpeed * interval  # Angle change per step

# Initial Position & Orientation
x, y = 500, 500  # Start at center
yaw = 0  # Initial orientation
points = [(x, y)]  # Flight path tracking

def get_live_location():
    """Fetch approximate real-time latitude & longitude based on IP. Defaults to BITS Pilani Hyd Campus, Block D."""
    g = geocoder.ip("me")  # Fetch location via IP
    return [17.5449, 78.5718]  


def update_map():
    """Generate map with the updated drone path"""
    lat, lon = get_live_location()
    print(f"Live Location: {lat}, {lon}")

    # Generate Folium Map
    live_map = folium.Map(location=[lat, lon], zoom_start=19)
    
    # Draw all path points
    for idx, (px, py) in enumerate(points):
        point_lat = lat + (py - 500) / 100000  # Approx. scaling for map accuracy
        point_lon = lon + (px - 500) / 100000
        folium.CircleMarker([point_lat, point_lon], radius=3, color="red").add_to(live_map)

    # Mark current position
    folium.Marker([lat, lon], popup="Drone", icon=folium.Icon(color="blue")).add_to(live_map)

    # Save and open map
    live_map.save("map.html")
    webbrowser.open("map.html")

def getKeyBoardInput():
    """Reads keyboard input and updates position & yaw."""
    global x, y, yaw

    lr, fb, yv = 0, 0, 0
    keys = pygame.key.get_pressed()

    # Movement Controls
    if keys[pygame.K_LEFT]:
        lr = -dInterval  # Move left  
    elif keys[pygame.K_RIGHT]:
        lr = dInterval  # Move right  

    if keys[pygame.K_UP]:
        fb = dInterval  # Move forward  
    elif keys[pygame.K_DOWN]:
        fb = -dInterval  # Move backward  

    # Rotation Controls (Yaw)
    if keys[pygame.K_a]:
        yv = -aInterval  # Rotate counterclockwise
        yaw -= aInterval  
    elif keys[pygame.K_d]:
        yv = aInterval  # Rotate clockwise
        yaw += aInterval  

    sleep(interval)

    # **Update Position based on Yaw**
    x += int(fb * math.cos(math.radians(yaw)) - lr * math.sin(math.radians(yaw)))
    y += int(fb * math.sin(math.radians(yaw)) + lr * math.cos(math.radians(yaw)))  

    return [x, y]

def drawPoints(img, points):
    """Draws flight path and position on the map."""
    for point in points:
        cv2.circle(img, point, 3, (0, 0, 255), cv2.FILLED)  # Red path (previous positions)
    
    # Green Circle for Current Position
    cv2.circle(img, points[-1], 6, (0, 255, 0), cv2.FILLED)  
    cv2.putText(img, f'({(points[-1][0]-500)/scale_factor:.2f}, {(500 - points[-1][1])/scale_factor:.2f}) ft',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)

while True:
    x, y = getKeyBoardInput()

    # Create Background Grid for Visualization
    img = np.zeros((1000, 1000, 3), np.uint8)
    for i in range(0, 1000, 100):
        cv2.line(img, (i, 0), (i, 1000), (50, 50, 50), 1)
        cv2.line(img, (0, i), (1000, i), (50, 50, 50), 1)

    # Update path only if position changes
    if (points[-1][0] != x) or (points[-1][1] != y):
        points.append((x, y))
    
    drawPoints(img, points)
    cv2.imshow('Drone Flight Path', img)

    # Press 'M' to update and show the map
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cv2.destroyAllWindows()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                update_map()

    cv2.waitKey(1)  