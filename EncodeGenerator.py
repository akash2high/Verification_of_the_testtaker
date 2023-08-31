import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate("FirebaseKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://verification-portal-dfb9d-default-rtdb.firebaseio.com/',
    'storageBucket': 'verification-portal-dfb9d.appspot.com'
}
                              )

#importing the face images:
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
ids = []
for path in pathList:
    # print(cv2.imread(os.path.join(folderPath,path)))
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    # print(os.path.splitext(path)[0]) #checking
    ids.append(os.path.splitext(path)[0])   #implementing

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


print(len(imgList))
print(ids)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return  encodeList

print("Encoding Started")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, ids]
print(encodeListKnown)
print("Encoding Completed")


file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")