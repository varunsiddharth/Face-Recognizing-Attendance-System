#!/usr/bin/env python3
"""
Setup script for CLASS VISION Attendance Management System
"""
import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating necessary directories...")
    directories = [
        'static',
        'TrainingImage',
        'TrainingImageLabel', 
        'StudentDetails',
        'Attendance'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"ℹ️  Directory already exists: {directory}")

def check_camera_access():
    """Check if camera is accessible"""
    print("\n📷 Checking camera access...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera is accessible")
            cap.release()
            return True
        else:
            print("⚠️  Camera not accessible - please check camera permissions")
            return False
    except ImportError:
        print("⚠️  OpenCV not installed yet - will check after installation")
        return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("🎓 CLASS VISION - Setup Script")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Setup failed during package installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Check camera access
    check_camera_access()
    
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python start_web_app.py")
    print("2. Open your browser to: http://localhost:5000")
    print("3. Start using the attendance system!")
    print()
    print("For help, check the README.md file")
    print("=" * 60)

if __name__ == "__main__":
    main()
