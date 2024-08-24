from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import cv2
import numpy as np
import face_recognition
import datetime

app = Flask(__name__)

# Enable CORS
CORS(app)

# Known faces dictionary (you can populate this with known faces and their corresponding names)
known_faces = {
    "images/ratantata_001.jpg": "ratantata",
    
    # Add more mappings as needed
}

# Directory to store attendance records
attendance_dir = 'attendance_records'
if not os.path.exists(attendance_dir):
    os.makedirs(attendance_dir)

# Set to keep track of recognized faces whose attendance has already been marked
marked_attendance = set()

# Function to mark attendance
def mark_attendance(name):
    # Get current date
    now = datetime.datetime.now()
    date = now.strftime('%Y-%m-%d')

    # Check if attendance has already been marked for the recognized face
    if name in marked_attendance:
        print(f"Attendance already marked for {name}")
        return jsonify({"acknowledged": f"Attendance already marked for {name}"}), 200

    # Check if attendance record already exists in the file
    attendance_record = f'{name},{date}'
    attendance_file = f'{attendance_dir}/attendance_{date}.txt'
    if os.path.exists(attendance_file):
        with open(attendance_file, 'r') as file:
            existing_records = file.readlines()
            if attendance_record in existing_records:
                print(f"Attendance already exists for {name} on {date}")
                marked_attendance.add(name)
                return jsonify({"acknowledged": f"Attendance already exists for {name} on {date}"}), 200

    # Write attendance to the file
    with open(attendance_file, 'a') as file:
        file.write(f'{attendance_record}\n')

    # Add the recognized face to the set of marked attendance
    marked_attendance.add(name)
    with open("attendancecheck.txt", 'w') as file:
        file.writelines(list(marked_attendance))

    # Print attendance marked message
    print(f"Attendance marked for {name}")
    return jsonify({"acknowledged": f"Attendance marked for {name}"}), 200

# Route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and attendance marking
@app.route('/upload', methods=['POST'])
def upload():
    try:
        uploaded_file = request.files['imageFile']
        
        # Process or save the uploaded file as needed
        
        # Save the uploaded image temporarily
        uploaded_image_path = 'uploaded_image.jpg'
        uploaded_file.save(uploaded_image_path)
        
        # Load the uploaded image
        uploaded_image = face_recognition.load_image_file(uploaded_image_path)
        
        # Detect faces in the uploaded image
        uploaded_face_locations = face_recognition.face_locations(uploaded_image)
        
        # Recognize faces and mark attendance
        for top, right, bottom, left in uploaded_face_locations:
            # Encode the face
            uploaded_face_encoding = face_recognition.face_encodings(uploaded_image, [(top, right, bottom, left)])[0]
            
            # Compare the face with known faces
            for known_image_path, known_name in known_faces.items():
                known_image = face_recognition.load_image_file(known_image_path)
                known_face_encoding = face_recognition.face_encodings(known_image)[0]
                match = face_recognition.compare_faces([known_face_encoding], uploaded_face_encoding)
                
                if match[0]:
                    # Mark attendance with the recognized name
                    return mark_attendance(known_name)
        
        return jsonify({"acknowledged": "Face not recognized"}), 200
    
    except Exception as e:
        print(f"Error processing upload: {e}")
        return jsonify({"acknowledged": "Upload failed"}), 400

if __name__ == '__main__':
    app.run(debug=True)

