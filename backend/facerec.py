import cv2
import face_recognition
import numpy as np
import os
import csv
from datetime import datetime

path = 'ATTENDANCE IMAGES'
image = []
classname = []
mylist = os.listdir(path)
print(f"Files in directory: {mylist}")

# Load images
for cl in mylist:
    curimg = cv2.imread(f'{path}/{cl}')
    if curimg is None:
        print(f"Error: Unable to load image {cl}. Skipping.")
        continue
    if len(curimg.shape) != 3 or curimg.shape[2] != 3:
        print(f"Error: Image {cl} is not a 3-channel RGB image. Skipping.")
        continue
    image.append(curimg)
    classname.append(os.path.splitext(cl)[0])
    print(f"Loaded image: {cl}")

now = datetime.now()
current_date = now.strftime('%d-%m-%Y')
processed_names = set()

f = open(current_date + '.csv', 'a+', newline='')
writer = csv.writer(f)

def findencoding(imagess):
    encodelist = []
    for img in imagess:
        if img is None:
            print("Skipping None image.")
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        encodings = face_recognition.face_encodings(img)
        if not encodings:
            print("No faces found in the image.")
        for encode in encodings:
            encodelist.append(encode)
    return encodelist

encodeknownlist = findencoding(image)
print(f"Encoding completed. Found {len(encodeknownlist)} encodings.")

cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to capture frame from webcam.")
        break

    sframes = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_sframe = cv2.cvtColor(sframes, cv2.COLOR_BGR2RGB)

    facescurframe = face_recognition.face_locations(rgb_sframe)
    encodecurframe = face_recognition.face_encodings(rgb_sframe, facescurframe)

    for encodefac, facloc in zip(encodecurframe, facescurframe):
        matches = face_recognition.compare_faces(encodeknownlist, encodefac)
        facdis = face_recognition.face_distance(encodeknownlist, encodefac)
        print(f"Face distances: {facdis}")
        matchIndex = np.argmin(facdis)

        if matches[matchIndex]:
            name = classname[matchIndex].capitalize()
            if name not in processed_names:
                y1, x2, y2, x1 = facloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, name, (x2 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (220, 20, 60), 2)

                current_time = now.strftime('%H-%M-%S')
                writer.writerow([name, current_time])

                processed_names.add(name)

                for _ in range(60):
                    success, temp_frame = cap.read()
                    cv2.imshow('webcam', frame)
                    if cv2.waitKey(1) & 0xFF == 27:
                        break

    cv2.imshow('webcam', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        print("Exiting program...")
        break

cap.release()
cv2.destroyAllWindows()
f.close()