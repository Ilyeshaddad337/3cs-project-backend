from flask import Flask, Response, send_file, redirect
from picamera2 import Picamera2
from datetime import datetime
import cv2
import os
import time

app = Flask(__name__)

# Shared Picamera2 instance
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

# Directories for photo storage
ORIGINAL_DIR = "original_photos"
os.makedirs(ORIGINAL_DIR, exist_ok=True)

# Remote machine credentials (edit this!)
LINUX_MACHINE_IP = "192.168.76.96"
LINUX_USERNAME = "ramzi-borz"
LINUX_PASSWORD = "2003"
LINUX_DESTINATION_PATH = "/home/ramzi-borz/pi/photos"  

def generate_frames():
    while True:
        frame = picam2.capture_array()
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return redirect('/capture')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    try:
        picam2.stop()

        config = picam2.create_still_configuration()
        picam2.configure(config)
        picam2.start()
        time.sleep(3)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_path = os.path.join(ORIGINAL_DIR, f"class_original_{timestamp}.jpg")
        picam2.capture_file(original_path)

        picam2.stop()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        picam2.start()

        return send_file(original_path, mimetype='image/jpeg')
    
    
    except Exception as e:
        return f"? Error: {e}<br><a href='/'>Back to Stream</a>"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

