import cv2
import numpy as np
import os
from face_recognition import train_model, recognize_face

# Load pre-trained face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load or train the face recognition model
face_model = train_model("path_to_preprocessed_images")

# Create a directory to store attendance records if it doesn't exist
attendance_dir = 'attendance_records'
if not os.path.exists(attendance_dir):
    os.makedirs(attendance_dir)

def mark_attendance(name):
    # Get current date
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')

    # Write attendance to a file
    with open(f'{attendance_dir}/attendance_{date}.txt', 'a') as file:
        file.write(f'{name},{date}\n')

# Load video capture device (webcam)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Recognize faces and mark attendance
    for (x, y, w, h) in faces:
        # Extract face region from the frame
        face_roi = gray[y:y+h, x:x+w]
        
        # Recognize the face
        name = recognize_face(face_roi, face_model)
        
        if name:
            mark_attendance(name)
    
    # Display the resulting frame
    cv2.imshow('Attendance Marking', frame)
    
    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
