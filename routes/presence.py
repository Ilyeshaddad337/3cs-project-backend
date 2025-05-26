
from flask import jsonify
from flask_jwt_extended import jwt_required
from models import Task, db
from app import app
from . import api
import threading
from model.detector import FaceDetector
from config import KNOWN_STUDENTS_DIR, TEST_IMG_PATH
# import requests
import os
import json


@api.route("/presence/<int:class_id>", methods=['POST'])
#@jwt_required()
def handle_presence(class_id):
    t = Task(result="")
    db.session.add(t)
    db.session.commit()

    thread = threading.Thread(target=process_presence, args=(class_id,t.id,))
    thread.start()
    return jsonify({
        "job_id": t.id,
        "status_url": f"/presence/status/{t.id}"
    }), 202

@api.route("/presence/status/<task_id>", methods=['GET'])
#@jwt_required()
def check_status(task_id):
    task_result = Task.query.filter_by(id=task_id).first()
    if (not task_result):
        return jsonify({"status": "NOT_FOUND", "error":"a task with that id does not exist!"}), 404
        
    if task_result.status == 'PENDING':
        return jsonify({"status": "pending"}), 202
    elif task_result.status == 'STARTED':
        return jsonify({"status": "processing"}), 202
    elif task_result.status == 'FINISHED':
        return jsonify({
            "status": "done",
            "result": json.loads(task_result.result)
        }), 200
    




def process_presence(class_id, task_id):            
    print("hello")
    with app.app_context():
        if (not task_id):
            return
        t = Task.query.filter_by(id=task_id).first()
        if (not t):
            return
        
        try:
            print(f"Detecting the faces for : {class_id}")
            # response = requests.get("http://CAMERA_API/capture")
            # image_path = save_image(response.content)  # save locally
            image_path = TEST_IMG_PATH
            detector = FaceDetector(KNOWN_STUDENTS_DIR)

            # Run face detection
            results = detector.detect_faces(image_path)
            # treat the names 
            results = [(name.split("_")[0] + " "+ name.split("_")[1] if len(name.split("_"))==2 else name) for name in results] 
            results = list(set(results))   
            t.result = json.dumps(results)
            t.status = "FINISHED"
            db.session.commit()
            # Save results to DB or return directly
            return 

        except Exception as e:
            try:
                print(f"Task {task_id} failed because: {str(e)}")
                t.status = "FAILED"
                t.result = json.dumps({
                    "error": str(e)
                })
                db.session.commit()
            except Exception as e2:
                print(f"Task {task_id} failed again because: {str(e2)}")

            return 
