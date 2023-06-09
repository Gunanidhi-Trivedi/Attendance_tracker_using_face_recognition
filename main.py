import face_recognition
import cv2
import numpy as np
import csv
import os
import datetime

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

dhoni_image = face_recognition.load_image_file("images/dhoni.jpg")
dhoni_face_encoding = face_recognition.face_encodings(dhoni_image)[0]

virat_image = face_recognition.load_image_file("images/Kohli.jpg")
virat_face_encoding = face_recognition.face_encodings(virat_image)[0]

known_face_encodings = [
    dhoni_face_encoding,
    virat_face_encoding
]

known_face_names = [
    "MS Dhoni",
    "Virat Kohli"
]

students = known_face_names.copy()

face_locations = []
face_encodings = []
face_names = []
s = True

now = datetime.datetime.now()
current_date = now.strftime("%d-%m-%Y")

f =    open('attendance.csv', 'w+', newline='')
lnwriter = csv.writer(f)

while True:
    _, frame = video_capture.read()
    samll_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = samll_frame[:, :, ::-1]
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            marches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = ""
            face_distence = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distence)
            if marches[best_match_index]:
                name = known_face_names[best_match_index]
                print(name)
            face_names.append(name)
            if name in known_face_names:
                if name in students:
                    print(students)
                    students.remove(name)
                    current_time = now.strftime("%H:%M:%S")
                    lnwriter.writerow([name, current_date, current_time])
        cv2.imshow("attendence system", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
video_capture.release()
cv2.destroyAllWindows()
f.close()




