import cv2
import sqlite3

cam=cv2.VideoCapture(0)
faceDetect=cv2.CascadeClassifier("face.xml")

def insertOrUpdate(id,Name):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM People WHERE ID="+str(id)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==1):
        cmd="UPDATE People SET Name=' "+str(name)+" ' WHERE ID="+str(id)
    else:
        cmd="INSERT INTO People(ID,Name) Values("+str(id)+",' "+str(name)+" ')"
    conn.execute(cmd)
    conn.commit()
    conn.close()
    
id=input('enter your id:');
name=input('enter your name:')
insertOrUpdate(id,name)
sampleNum=0
while(True):
    ret,img = cam.read()
    #cv2.imshow('image',img)
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        sampleNum=sampleNum+1;
        cv2.imwrite("dataSet/User."+str(id) +'.'+str(sampleNum)+ ".jpg",gray[y:y+h,x:x+w])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)  
        cv2.waitKey(100);
    cv2.imshow('Face',img);
    cv2.waitKey(100)&0xff;
    if(sampleNum>20) :
        break
cam.release()
cv2.destroyAllWindows()
