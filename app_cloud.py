#!/usr/bin/env python3
"""
Cloud-friendly version of CLASS VISION Attendance Management System
This version works on cloud platforms without camera access
"""
from flask import Flask, render_template, request, jsonify
import os
import csv
import pandas as pd
import datetime
import time
import json

app = Flask(__name__)

# Create necessary directories
os.makedirs('static', exist_ok=True)
os.makedirs('TrainingImage', exist_ok=True)
os.makedirs('TrainingImageLabel', exist_ok=True)
os.makedirs('StudentDetails', exist_ok=True)
os.makedirs('Attendance', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Global variables
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

@app.route('/')
def index():
    """Main page"""
    return render_template('index_cloud.html')

@app.route('/register')
def register():
    """Registration page"""
    return render_template('register_cloud.html')

@app.route('/attendance')
def attendance():
    """Attendance page"""
    return render_template('attendance_cloud.html')

@app.route('/view_attendance')
def view_attendance():
    """View attendance page"""
    return render_template('view_attendance_cloud.html')

@app.route('/api/register_student', methods=['POST'])
def register_student():
    """API endpoint to register a new student"""
    try:
        data = request.get_json()
        enrollment = data.get('enrollment', '').strip()
        name = data.get('name', '').strip()
        
        if not enrollment or not name:
            return jsonify({'success': False, 'message': 'Enrollment number and name are required'})
        
        # Save student details to CSV
        row = [enrollment, name]
        with open(studentdetail_path, "a+", newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=",")
            writer.writerow(row)
        
        return jsonify({'success': True, 'message': f'Student {name} registered successfully'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/api/mark_attendance', methods=['POST'])
def mark_attendance():
    """API endpoint to mark attendance manually"""
    try:
        data = request.get_json()
        subject = data.get('subject', '').strip()
        student_id = data.get('student_id', '').strip()
        student_name = data.get('student_name', '').strip()
        
        if not subject or not student_id or not student_name:
            return jsonify({'success': False, 'message': 'All fields are required'})
        
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

@app.route('/api/get_students')
def get_students():
    """API endpoint to get all registered students"""
    try:
        if not os.path.exists(studentdetail_path):
            return jsonify({'success': True, 'students': []})
        
        df = pd.read_csv(studentdetail_path)
        students = df.to_dict('records')
        return jsonify({'success': True, 'students': students})
        
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
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
