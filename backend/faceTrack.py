import cv2
import numpy as np
from djitellopy import tello
from time import sleep

# Initialize the Tello drone
drone = tello.Tello()

drone.connect()
drone.streamon()
drone.takeoff()

drone.send_rc_control(0,0,60,0)

# Drone control settings
w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.6, 0.5, 0]  # PID controller constants
pError = 0

# Load Haar Cascade for face detection
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def findFace(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Reduce scaleFactor and minNeighbors for faster detection
    faces = faceCascade.detectMultiScale(imgGray, scaleFactor=1.05, minNeighbors=4, minSize=(30, 30))

    myFacelist = []  # List of faces detected
    myFacelistArea = []  # Corresponding areas of the detected faces

    for (x, y, w, h) in faces:
        cx, cy = x + w // 2, y + h // 2
        area = w * h
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFacelist.append([cx, cy])
        myFacelistArea.append(area)

    if myFacelistArea:
        i = myFacelistArea.index(max(myFacelistArea))
        return img, [myFacelist[i], myFacelistArea[i]]
    else:
        return img, [[0, 0], 0]

def trackFace(info, w, pid, pError):
    x, y = info[0]
    area = info[1]
    error = x - w // 2
    fb = 0

    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    # Adjust fb (forward/backward movement)
    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        fb = 0
        error = 0

    # Send control commands
    drone.send_rc_control(0, fb, 0, speed)

    return error

# Start controlling drone
while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)
    cv2.imshow("Output", img)
    
    # Adjust frame display speed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()
        break
