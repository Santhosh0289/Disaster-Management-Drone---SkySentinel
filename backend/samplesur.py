import keypress as kp
from djitellopy import tello
import time 
import cv2 

kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
global img
drone.streamon()

def getKeyBoardInput():
    lr, fb, ud, yv = 0,0,0,0
    speed = 150

    if kp.getKey("LEFT"): lr = -speed
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    elif kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    elif kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yv = -speed
    elif kp.getKey("d"): yv= speed

    if kp.getKey("q"): drone.land()
    if kp.getKey("e"): drone.takeoff()

    if kp.getKey("t"): cv2.imwrite(f'image/{time.time()}.jpg',img); time.sleep(0.3)

    return[lr, fb, ud, yv]



while True:
    vals = getKeyBoardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = drone.get_frame_read().frame
    img = cv2.resize(img,(600, 600))
    cv2.imshow("image",img)
    cv2.waitKey(1)