#!/usr/bin/env python3
"""
Startup script for the Attendance Management System Web Application
"""
import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open the web browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

def main():
    print("=" * 60)
    print("🎓 CLASS VISION - Attendance Management System")
    print("=" * 60)
    print()
    print("Starting web application...")
    print("📱 Web Interface: http://localhost:5000")
    print("🔧 API Endpoints: http://localhost:5000/api/")
    print()
    print("Features:")
    print("✅ Web-based camera capture (no more black screen!)")
    print("✅ Real-time face recognition")
    print("✅ Modern responsive interface")
    print("✅ Cross-platform compatibility")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Open browser automatically
    Timer(3.0, open_browser).start()
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

