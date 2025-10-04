# 🎓 CLASS VISION - Face Recognition Attendance Management System

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/opencv-4.0+-red.svg)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern web-based attendance management system using face recognition technology. This system eliminates the common issues with desktop applications like black screens, camera access problems, and interface limitations.

## ✨ Features

### 🎯 **Core Functionality**
- **Face Recognition**: Advanced face detection and recognition using OpenCV
- **Web-Based Interface**: Modern, responsive web application
- **Real-Time Camera**: Live camera preview with face detection overlay
- **Attendance Tracking**: Subject-wise attendance management
- **Data Export**: CSV export functionality for attendance records

### 🚀 **Key Advantages**
- ✅ **No More Black Screens**: Web-based camera with live preview
- ✅ **Cross-Platform**: Works on Windows, Mac, Linux
- ✅ **Modern UI**: Responsive design that works on all devices
- ✅ **Real-Time Feedback**: Live progress tracking and status updates
- ✅ **Easy Setup**: Simple installation and configuration

## 🖥️ Screenshots

### Home Dashboard
![Home Dashboard](Project%20Snap/1.PNG)

### Student Registration
![Student Registration](Project%20Snap/2.PNG)

### Face Capture Process
![Face Capture](Project%20Snap/3.PNG)

### Attendance Taking
![Attendance Taking](Project%20Snap/4.PNG)

### Attendance Records
![Attendance Records](Project%20Snap/5.PNG)

## 🚀 Quick Start

### Prerequisites
- Python 3.6 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Webcam or camera device

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/attendance-management-system.git
   cd attendance-management-system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the application**
   ```bash
   python start_web_app.py
   ```

4. **Open your browser**
   - Go to: `http://localhost:5000`
   - The application will automatically open in your default browser

## 📖 How to Use

### 1. Register Students
1. Click **"Register Student"** on the home page
2. Enter student's enrollment number and full name
3. Click **"Start Image Capture"**
4. Position the student in front of the camera
5. Click **"Capture Image"** repeatedly (50 times recommended)
6. Click **"Train Model"** to train the recognition system

### 2. Take Attendance
1. Click **"Take Attendance"** on the home page
2. Enter the subject name
3. Click **"Start Attendance"**
4. Position students in front of the camera
5. Click **"Recognize Face"** to mark attendance
6. View real-time attendance log

### 3. View Attendance Records
1. Click **"View Attendance"** on the home page
2. Select or enter subject name
3. View detailed attendance statistics
4. Export data as CSV if needed

## 🏗️ Project Structure

```
attendance-management-system/
├── app.py                      # Main Flask application
├── start_web_app.py           # Easy startup script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── templates/                 # HTML templates
│   ├── index.html            # Home page
│   ├── register.html         # Student registration
│   ├── attendance.html       # Take attendance
│   └── view_attendance.html  # View records
├── static/                    # Static files (auto-created)
├── TrainingImage/            # Student face images
├── TrainingImageLabel/       # Trained model files
├── StudentDetails/           # Student information
├── Attendance/              # Attendance records
└── Project Snap/            # Screenshots
```

## 🔧 Technical Details

### Backend Technologies
- **Flask**: Web framework for Python
- **OpenCV**: Computer vision and face recognition
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **PIL**: Image processing

### Frontend Technologies
- **HTML5**: Modern markup
- **CSS3**: Responsive styling with gradients and animations
- **JavaScript**: Client-side functionality
- **WebRTC**: Camera access and video streaming

### API Endpoints
- `GET /` - Home page
- `GET /register` - Student registration page
- `GET /attendance` - Take attendance page
- `GET /view_attendance` - View attendance page
- `POST /api/capture_images` - Register new student
- `POST /api/save_image` - Save captured face image
- `POST /api/train_model` - Train recognition model
- `POST /api/recognize_face` - Recognize face in image
- `POST /api/mark_attendance` - Mark attendance
- `GET /api/get_attendance/<subject>` - Get attendance records

## 🛠️ Configuration

### Camera Settings
The application automatically configures camera settings for optimal performance:
- Resolution: 640x480
- Frame rate: 30 FPS
- Backend: DirectShow (Windows) with fallback

### Face Recognition Settings
- Algorithm: LBPH (Local Binary Patterns Histograms)
- Confidence threshold: 70%
- Minimum face size: 30x30 pixels
- Training samples: 50 images per student (recommended)

## 🔒 Security & Privacy

- **Local Processing**: All face recognition happens locally on your machine
- **No Cloud Storage**: No data is sent to external servers
- **Secure Access**: Web interface runs on localhost only
- **Data Control**: You have complete control over all data

## 🐛 Troubleshooting

### Common Issues

**Camera not working:**
- Ensure browser has camera permissions
- Try refreshing the page
- Check if other applications are using the camera
- Try a different browser

**Face recognition not working:**
- Ensure good lighting conditions
- Face the camera directly
- Make sure student is registered first
- Capture more training images (closer to 50)

**Server won't start:**
- Check if port 5000 is available
- Try: `python -m flask run --port 5001`
- Ensure all dependencies are installed

**Images not capturing:**
- Check browser console for errors (F12)
- Ensure camera permissions are granted
- Try a different browser
- Check internet connection

### Performance Optimization

**For better recognition accuracy:**
- Use good lighting conditions
- Capture images from different angles
- Ensure face is clearly visible
- Avoid shadows and reflections

**For better performance:**
- Close other applications using the camera
- Use a modern browser
- Ensure stable internet connection
- Use a dedicated camera if possible

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 7+, macOS 10.12+, Ubuntu 16.04+
- **Python**: 3.6 or higher
- **RAM**: 4GB
- **Storage**: 1GB free space
- **Camera**: USB webcam or built-in camera

### Recommended Requirements
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 8GB
- **Storage**: 2GB free space
- **Camera**: HD webcam with good lighting

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenCV** for computer vision capabilities
- **Flask** for the web framework
- **Haar Cascade** for face detection
- **Contributors** who helped improve this project

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** above
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Contact support** for urgent matters

## 🔄 Version History

### v2.0.0 (Current)
- ✅ Web-based interface
- ✅ Real-time camera preview
- ✅ Modern responsive design
- ✅ Cross-platform compatibility
- ✅ Enhanced face recognition
- ✅ Improved user experience

### v1.0.0 (Legacy)
- Desktop application
- Tkinter interface
- Windows-specific
- Camera access issues

## 🎯 Roadmap

### Upcoming Features
- [ ] Mobile app support
- [ ] Cloud synchronization
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Integration with LMS systems
- [ ] Advanced reporting features

---

**Made with ❤️ for educational institutions worldwide**

*For more information, visit our [GitHub repository](https://github.com/yourusername/attendance-management-system)*
