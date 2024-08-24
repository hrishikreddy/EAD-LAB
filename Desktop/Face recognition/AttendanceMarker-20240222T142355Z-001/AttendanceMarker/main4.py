import cv2
import os
import datetime
import face_recognition

# Database of known faces and corresponding exam names
known_faces = {
    "images/ratantata_001.jpg": "ratan tata",
    # Add more mappings as needed
}

# Create a directory to store attendance records if it doesn't exist
attendance_dir = 'attendance_records'
if not os.path.exists(attendance_dir):
    os.makedirs(attendance_dir)

# Set to keep track of recognized faces whose attendance has already been marked
marked_attendance ={}
with open("attendancecheck.txt", 'r') as file:
  marked_attendance =set( file.readlines())
 
# Function to mark attendance
def mark_attendance(name):
    # Get current date
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')

    # Check if attendance has already been marked for the recognized face
    if name in marked_attendance:
        print(f"Attendance already marked for {name}")
        return

    # Check if attendance record already exists in the file
    attendance_record = f'{name},{date}'
    attendance_file = f'{attendance_dir}/attendance_{date}.txt'
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as file:
            existing_records = file.readlines()
            if attendance_record in existing_records:
                print(f"Attendance already exists for {name} on {date}")
                marked_attendance.add(name)
                return

    # Write attendance to the file
    with open(attendance_file, 'a') as file:
        file.write(f'{attendance_record}\n')

    # Add the recognized face to the set of marked attendance
    marked_attendance.add(name)
    with open("attendancecheck.txt", 'w') as file:
      file.writelines(list(marked_attendance))

    # Print attendance marked message
    print(f"Attendance marked for {name}")

# Load video capture device (webcam)
cap = cv2.VideoCapture(0)
while True:
    # Reset exam_name at the beginning of each iteration
    exam_name = None

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to RGB (face_recognition library expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

    # Recognize faces and mark attendance
    for top, right, bottom, left in face_locations:
        # Extract face region from the frame
        face_roi = frame[top:bottom, left:right]

        # Encode the face
        unknown_face_encoding = face_recognition.face_encodings(rgb_frame, [(top, right, bottom, left)])[0]

        # Compare the face with known faces
        for known_image_path, known_name in known_faces.items():
            known_image = face_recognition.load_image_file(known_image_path)
            known_face_encodings = face_recognition.face_encodings(known_image)
            for known_face_encoding in known_face_encodings:
                match = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding, tolerance=0.5)
                if match[0]:
                    exam_name = known_name
                    break
            if exam_name:
                break

        if exam_name:
            # Mark attendance with the recognized exam name
            mark_attendance(exam_name)
            break

    # Display the resulting frame
    cv2.imshow('Attendance Marking', frame)

    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
