import os
import pickle
from datetime import datetime

import cv2
import cvzone
import face_recognition
import numpy as np
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("FirebaseKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://verification-portal-dfb9d-default-rtdb.firebaseio.com/',
    'storageBucket': 'verification-portal-dfb9d.appspot.com'
}
                              )
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background (2).png')

#importing the Modes images:
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))

#load the encoding file

print("Loading Encode file ....")
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
encodeListKnown, ids = encodeListKnownWithIds
print(ids)
print("Encode file loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("face", faceDis)

            matchIndex = np.argmin(faceDis)
            print("Student Id", ids[matchIndex])
            print(faceDis[matchIndex])

            if faceDis[matchIndex] < 0.45:
                # print("Known Face Detected", ids[matchIndex])
                y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 25 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cv2.rectangle(imgBackground, bbox, color=(255, 0, 0), thickness=2)
                id = ids[matchIndex]
                # imgBackground= cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                imgBackground = cv2.rectangle(imgBackground, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)

                cv2.putText(imgBackground, str(id), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (27, 27, 27), 2)
                if counter == 0:
                    counter = 1
                    modeType = 1
            else:
                id = "Unknown"
                y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 25 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cv2.rectangle(imgBackground, bbox, color=(255, 0, 0), thickness=2)
                # id = ids[matchIndex]
                # imgBackground= cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # imgBackground = cv2.rectangle(img, bbox, cv2.FILLED)
                cv2.rectangle(imgBackground, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgBackground, id, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (27, 27, 27), 2)



        if counter != 0:
            if counter == 1:
                # get the data
                studentInfo = db.reference(f'TestTaker/{id}').get()  # realtime database name
                print(studentInfo)
                # get the image
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                datetimeObject = datetime.strptime(studentInfo['last_login_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)

                if secondsElapsed > 30:

                    ref = db.reference(f'TestTaker/{id}')
                    # studentInfo['total_attendance'] +=1
                    # ref.child('total_attendance').set(studentInfo['total_attendance'])

                    ref.child('last_login_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            if modeType != 3:
                if 10 < counter < 20:
                    modeType = 2
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['name']), (861, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (27, 27, 27), 1)
                    cv2.putText(imgBackground, str(studentInfo['course']), (1006, 550),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (27, 27, 27), 1)
                    cv2.putText(imgBackground, str(ids[matchIndex]), (1006, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (27, 27, 27), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1099, 625),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (27, 27, 27), 1)
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                # for center aligning the name text
                #             cv2.FONT_HERSHEY_COMPLEX, 0.5,(27, 27, 27), 1)
                # offset = (414-w)//2

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("FaceTest", imgBackground)
    cv2.waitKey(1)