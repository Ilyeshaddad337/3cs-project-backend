
from flask import jsonify
from flask_jwt_extended import jwt_required
from models import Task, db, Classe
from app import app
from . import api
import threading
import uuid
from model.detector import FaceDetector
from config import KNOWN_STUDENTS_DIR, TEST_IMG_PATH, HARDWARE_IP, OUTPUT_FOLDER
import requests
import os
import json


@api.route("/test", methods=['GET'])
def test_route():
    g = Classe.query.first()
    g = [{"name": s.name} for s in g.students ]
    return jsonify({"message": g}), 200


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
    with app.app_context():
        if (not task_id):
            return
        t = Task.query.filter_by(id=task_id).first()
        if (not t):
            return
        t.status = "STARTED"
        db.session.commit()
        try:
            print(f"Detecting the faces for : {class_id}")
            response = requests.get(HARDWARE_IP+"/capture")
            rnd_name = str(uuid.uuid4())
            if response.status_code == 200:
                rnd_name = str(uuid.uuid4())
                
                with open(os.path.join(OUTPUT_FOLDER,rnd_name+'.jpg'), 'wb') as f:
                    f.write(response.content)
                print(f"Image saved successfully as '{rnd_name}.jpg'")
            else:
                print(f"Failed to retrieve image. Status code: {response.status_code}")
                t.status = "FAILED"
                t.result = json.dumps({
                    "error": "Failed to retrieve image from hardware."
                })
                db.session.commit()
                return

            # # image_path = save_image(response.content)  # save locally
            # image_path = TEST_IMG_PATH
            detector = FaceDetector(KNOWN_STUDENTS_DIR)
            group = Classe.query.filter_by(id=class_id).first()
            if (not group):
                t.status = "FAILED"
                t.result = json.dumps({
                    "error": "Class not found."
                })
                db.session.commit()
                return
            group_students =  [s.name.lower() for s in group.students ]

            # Run face detection
            results = detector.detect_faces(os.path.join(OUTPUT_FOLDER,rnd_name+'.jpg'))
            # treat the names 
            results = [(name.split("_")[0] + " "+ name.split("_")[1] if len(name.split("_"))==2 else name) for name in results]
            results = [name  for name in results if name.lower() in group_students] 
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
