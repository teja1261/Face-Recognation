import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3

recognizer=cv2.face.LBPHFaceRecognizer_create();
recognizer.read("recognizer/trainner.yml")
cascadePath="face.xml"
faceCascade=cv2.CascadeClassifier(cascadePath);
path='dataSet'

def getProfile(id):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

cam=cv2.VideoCapture(0)
font=cv2.FONT_HERSHEY_COMPLEX_SMALL
while True:
    ret,img=cam.read();
    #cv2.imshow('image',img)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100,100));
    for(x,y,w,h) in faces:
        id,confidence= recognizer.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        if(confidence<100):
            profile=getProfile(id)
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            profile="unknown"
            confidence = "  {0}%".format(round(100 - confidence))    
        profile=getProfile(id)
        #print(str(profile))
        if(profile!=None):
            cv2.putText(img,"Id: "+str(profile[0]),(x,y+h+15),font,1.0,(255,255,255))
            cv2.putText(img,"Name:"+str(profile[1]),(x,y+h+30),font,1.0,(255,255,255))
            cv2.putText(img,"Age:"+str(profile[2]),(x,y+h+45),font,1.0,(255,255,255))
            cv2.putText(img,"Gender:"+str(profile[3]),(x,y+h+60),font,1.0,(255,255,255))
            cv2.putText(img,"Criminal records:"+str(profile[4]),(x,y+h+75),font,1.0,(255,255,255))
            cv2.putText(img, str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)
    cv2.imshow('img',img) 
    k = cv2.waitKey(30)&0xff
    if k == 27: # press 'ESC' to quit
        break
    
