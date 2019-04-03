#!/usr/bin/env python 
#coding=utf-8
#从目录中读取一堆文件

import face_recognition
import cv2
import os
import RPi.GPIO
import time

RPi.GPIO.setmode(RPi.GPIO.BCM)

RPi.GPIO.setwarnings(False)

buzzer=4
RPi.GPIO.setup(buzzer,RPi.GPIO.OUT)

RPi.GPIO.output(buzzer,True)

strangerAppear=False
strangerNum=0


demo_filelist=[]
demo_face_encodings=[]
demo_face_names=[]
for f in os.listdir('/home/pi/demo/face_recognition/jpg//'):
    demo_filelist.append(f)
    demo_face_names.append(f[:-4])

for filename in demo_filelist:
    print(u'正在加载....'+filename)
    demo_image = face_recognition.load_image_file('/home/pi/demo/face_recognition/jpg//'+filename)
    face_encoding = face_recognition.face_encodings(demo_image)[0]
    demo_face_encodings.append(face_encoding)

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = 1

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)

    # Only process every other frame of video to save time
    if process_this_frame==1:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
   #     print(u"我检测到了{}张脸。".format(len(face_locations)))
        face_names = []
        for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces(demo_face_encodings, face_encoding,tolerance=0.6)#
            print(match)
            name = "Unknown"
            i=-1
            for m in match:
                i+=1
                if m:
                    name= demo_face_names[i]

            if(name=="Unknown"):
                RPi.GPIO.output(buzzer,False)
                frame_1=cv2.flip(frame,1)
                path="/home/pi/demo/face_recognition/"+str(strangerNum)+".png"
                cv2.imwrite(path,frame_1)
                strangerNum=strangerNum+1
                strangerAppear=True
            face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a box around the face
        #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
#        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 5)
        font = cv2.FONT_HERSHEY_DUPLEX#FONT_HERSHEY_DUPLEX
#        print(name)
#        boxsize, _ = cv2.getTextSize(fs.string, fs.face, fs.fsize, fs.thick)
 #       locx = int((right+left)/2-25 - 14*len(name)/2)
        cv2.putText(frame, name, (20,20), font, 1.0, (0, 0, 255), 1)

    process_this_frame += 1# not process_this_frame
    if process_this_frame>1:
        process_this_frame=1
    # Display the resulting image

    ############
    cv2.imshow('Video', frame)
    cv2.moveWindow('Video',600,10)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        RPi.GPIO.output(buzzer,True)
        strangerAppear=False
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
