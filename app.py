#!/usr/bin/env python3
"""
Flask Web Application for Attendance Management System
"""
from flask import Flask, render_template, request, jsonify, send_file
import cv2
import numpy as np
import os
import csv
import pandas as pd
import datetime
import time
import base64
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories
os.makedirs('uploads', exist_ok=True)
os.makedirs('TrainingImage', exist_ok=True)
os.makedirs('TrainingImageLabel', exist_ok=True)
os.makedirs('StudentDetails', exist_ok=True)
os.makedirs('Attendance', exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Global variables
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

class FaceRecognitionSystem:
    def __init__(self):
        self.recognizer = None
        self.detector = cv2.CascadeClassifier(haarcasecade_path)
        self.load_recognizer()
    
    def load_recognizer(self):
        """Load the trained face recognizer"""
        try:
            if os.path.exists(trainimagelabel_path):
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.recognizer.read(trainimagelabel_path)
                return True
        except Exception as e:
            print(f"Error loading recognizer: {e}")
        return False
    
    def detect_faces(self, image):
        """Detect faces in an image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30))
        return faces, gray
    
    def recognize_face(self, face_image):
        """Recognize a face using the trained model"""
        if self.recognizer is None:
            return None, 0
        
        try:
            id, confidence = self.recognizer.predict(face_image)
            return id, confidence
        except:
            return None, 0
    
    def train_model(self):
        """Train the face recognition model"""
        try:
            faces, ids = self.get_images_and_labels()
            if len(faces) == 0:
                return False, "No training images found"
            
            if len(faces) < 2:
                return False, "Not enough training images"
            
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.train(faces, np.array(ids))
            self.recognizer.save(trainimagelabel_path)
            return True, f"Model trained successfully with {len(faces)} samples"
            
        except Exception as e:
            return False, f"Training failed: {str(e)}"
    
    def get_images_and_labels(self):
        """Get all training images and their labels"""
        faces = []
        ids = []
        
        try:
            if not os.path.exists(trainimage_path):
                return faces, ids
                
            student_dirs = [d for d in os.listdir(trainimage_path) if os.path.isdir(os.path.join(trainimage_path, d))]
            
            for student_dir in student_dirs:
                student_path = os.path.join(trainimage_path, student_dir)
                image_files = [f for f in os.listdir(student_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                
                for image_file in image_files:
                    try:
                        image_path = os.path.join(student_path, image_file)
                        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                        if image is not None:
                            filename_parts = image_file.split("_")
                            if len(filename_parts) >= 2:
                                id = int(filename_parts[1])
                                faces.append(image)
                                ids.append(id)
                    except Exception as e:
                        print(f"Error processing image {image_file}: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"Error in get_images_and_labels: {str(e)}")
            
        return faces, ids

# Initialize the face recognition system
face_system = FaceRecognitionSystem()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/register')
def register():
    """Registration page"""
    return render_template('register.html')

@app.route('/attendance')
def attendance():
    """Attendance page"""
    return render_template('attendance.html')

@app.route('/view_attendance')
def view_attendance():
    """View attendance page"""
    return render_template('view_attendance.html')

@app.route('/api/capture_images', methods=['POST'])
def capture_images():
    """API endpoint to capture and save images"""
    try:
        data = request.get_json()
        enrollment = data.get('enrollment', '').strip()
        name = data.get('name', '').strip()
        
        if not enrollment or not name:
            return jsonify({'success': False, 'message': 'Enrollment number and name are required'})
        
        # Create student directory
        directory = f"{enrollment}_{name}"
        path = os.path.join(trainimage_path, directory)
        
        if os.path.exists(path):
            return jsonify({'success': False, 'message': 'Student data already exists'})
        
        os.makedirs(path, exist_ok=True)
        
        # Save student details to CSV
        with open(studentdetail_path, "a+", newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow([enrollment, name])
        
        return jsonify({'success': True, 'message': 'Student registered successfully', 'path': path})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/save_image', methods=['POST'])
def save_image():
    """API endpoint to save a captured image"""
    try:
        data = request.get_json()
        image_data = data.get('image', '')
        enrollment = data.get('enrollment', '')
        name = data.get('name', '')
        image_number = data.get('image_number', 0)
        
        if not image_data or not enrollment or not name:
            return jsonify({'success': False, 'message': 'Missing required data'})
        
        # Decode base64 image
        image_data = image_data.split(',')[1]  # Remove data:image/jpeg;base64, prefix
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'success': False, 'message': 'Invalid image data'})
        
        # Detect and crop face
        faces, gray = face_system.detect_faces(image)
        
        if len(faces) == 0:
            return jsonify({'success': False, 'message': 'No face detected in image'})
        
        # Use the first detected face
        x, y, w, h = faces[0]
        face_img = gray[y:y+h, x:x+w]
        
        if face_img.size == 0:
            return jsonify({'success': False, 'message': 'Invalid face crop'})
        
        # Save the face image
        directory = f"{enrollment}_{name}"
        path = os.path.join(trainimage_path, directory)
        filename = f"{name}_{enrollment}_{image_number}.jpg"
        filepath = os.path.join(path, filename)
        
        cv2.imwrite(filepath, face_img)
        
        return jsonify({'success': True, 'message': f'Image {image_number} saved successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error saving image: {str(e)}'})

@app.route('/api/train_model', methods=['POST'])
def train_model():
    """API endpoint to train the face recognition model"""
    try:
        success, message = face_system.train_model()
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/recognize_face', methods=['POST'])
def recognize_face():
    """API endpoint to recognize a face"""
    try:
        data = request.get_json()
        image_data = data.get('image', '')
        
        if not image_data:
            return jsonify({'success': False, 'message': 'No image data provided'})
        
        # Decode base64 image
        image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return jsonify({'success': False, 'message': 'Invalid image data'})
        
        # Detect faces
        faces, gray = face_system.detect_faces(image)
        
        if len(faces) == 0:
            return jsonify({'success': False, 'message': 'No face detected'})
        
        # Recognize the first face
        x, y, w, h = faces[0]
        face_img = gray[y:y+h, x:x+w]
        
        if face_system.recognizer is None:
            return jsonify({'success': False, 'message': 'Model not trained yet'})
        
        id, confidence = face_system.recognize_face(face_img)
        
        if id is not None and confidence < 70:
            # Get student name from CSV
            try:
                df = pd.read_csv(studentdetail_path)
                student_name = df.loc[df['Enrollment'] == id]['Name'].values
                if len(student_name) > 0:
                    return jsonify({
                        'success': True, 
                        'recognized': True,
                        'id': int(id),
                        'name': student_name[0],
                        'confidence': float(confidence)
                    })
            except:
                pass
        
        return jsonify({'success': True, 'recognized': False, 'message': 'Face not recognized'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/mark_attendance', methods=['POST'])
def mark_attendance():
    """API endpoint to mark attendance"""
    try:
        data = request.get_json()
        subject = data.get('subject', '').strip()
        student_id = data.get('student_id', '')
        student_name = data.get('student_name', '')
        
        if not subject:
            return jsonify({'success': False, 'message': 'Subject name is required'})
        
        if not student_id or not student_name:
            return jsonify({'success': False, 'message': 'Student information is required'})
        
        # Create attendance record
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        
        # Create subject directory
        subject_path = os.path.join(attendance_path, subject)
        os.makedirs(subject_path, exist_ok=True)
        
        # Create attendance file
        filename = f"{subject}_{date}_{timeStamp.replace(':', '-')}.csv"
        filepath = os.path.join(subject_path, filename)
        
        # Check if file exists, if not create with headers
        if not os.path.exists(filepath):
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Enrollment', 'Name', date])
        
        # Add attendance record
        with open(filepath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([student_id, student_name, 1])
        
        return jsonify({
            'success': True, 
            'message': f'Attendance marked for {student_name}',
            'date': date,
            'time': timeStamp
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/get_attendance/<subject>')
def get_attendance(subject):
    """API endpoint to get attendance records for a subject"""
    try:
        subject_path = os.path.join(attendance_path, subject)
        if not os.path.exists(subject_path):
            return jsonify({'success': False, 'message': 'Subject not found'})
        
        # Get all CSV files for the subject
        csv_files = [f for f in os.listdir(subject_path) if f.endswith('.csv')]
        
        if not csv_files:
            return jsonify({'success': False, 'message': 'No attendance records found'})
        
        # Read and merge all CSV files
        dfs = []
        for csv_file in csv_files:
            df = pd.read_csv(os.path.join(subject_path, csv_file))
            dfs.append(df)
        
        if not dfs:
            return jsonify({'success': False, 'message': 'No data found'})
        
        # Merge all dataframes
        merged_df = dfs[0]
        for df in dfs[1:]:
            merged_df = merged_df.merge(df, how='outer', on=['Enrollment', 'Name'])
        
        # Fill NaN values with 0
        merged_df.fillna(0, inplace=True)
        
        # Calculate attendance percentage
        date_columns = [col for col in merged_df.columns if col not in ['Enrollment', 'Name']]
        if date_columns:
            merged_df['Attendance_Percentage'] = merged_df[date_columns].mean(axis=1) * 100
            merged_df['Attendance_Percentage'] = merged_df['Attendance_Percentage'].round(2)
        
        # Convert to list of dictionaries
        records = merged_df.to_dict('records')
        
        return jsonify({'success': True, 'records': records})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    print("Starting Attendance Management System Web Application...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
