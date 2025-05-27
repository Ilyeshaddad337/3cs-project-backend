from flask import Flask, Response, send_file
from picamera2 import Picamera2
from datetime import datetime
import cv2
import threading
import os
import time
import paramiko

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
    return '''
    <html>
    <head><title>Raspberry Pi Camera Stream</title></head>
    <body>
        <h1>Live Stream</h1>
        <img src="/video_feed" width="640" height="480" />
        <p><a href="/capture">? Capture High-Res Class Photo</a></p>
    </body>
    </html>
    '''

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    try:
        # Stop the camera before changing config
        picam2.stop()

        # Configure for still photo capture
        config = picam2.create_still_configuration()
        picam2.configure(config)
        picam2.start()
        time.sleep(3)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_path = os.path.join(ORIGINAL_DIR, f"class_original_{timestamp}.jpg")
        picam2.capture_file(original_path)

        # Stop and reconfigure for streaming again
        picam2.stop()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        picam2.start()

        #success = send_photo_sftp(
        #     local_path=original_path,
        #     remote_ip=LINUX_MACHINE_IP,
        #     remote_user=LINUX_USERNAME,
        #     remote_password=LINUX_PASSWORD,
        #     remote_path=LINUX_DESTINATION_PATH
        # )

        # return f"? Photo captured and sent: {success}<br><a href='/'>Back to Stream</a>"
        return send_file(original_path, mimetype='image/jpeg')
    
    
    except Exception as e:
        return f"? Error: {e}<br><a href='/'>Back to Stream</a>"


def send_photo_sftp(local_path, remote_ip, remote_user, remote_password, remote_path):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(remote_ip, username=remote_user, password=remote_password)
        sftp = ssh.open_sftp()
        filename = os.path.basename(local_path)
        remote_file_path = os.path.join(remote_path, filename)
        sftp.put(local_path, remote_file_path)
        sftp.close()
        ssh.close()
        return True
    except Exception as e:
        print(f"SFTP Error: {e}")
        return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

