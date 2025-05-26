from model.detector import FaceDetector
from config import KNOWN_STUDENTS_DIR, TEST_IMG_PATH
# import requests
import os
from models import Task, db
import json
def save_image():
    pass
def process_presence(class_id, task_id):
    with current_app.app_context():
            
        print("hello")
        if (not task_id):
            return
        t = Task.query.filterby(id=task_id).first()
        if (not t):
            return
        t.result = json.dumps({"list": [1 , 2 , 3]})
        t.status = "FINISHED"
        db.session.commit()
        return 
    # try:
    #     print(f"Detecting the faces for : {class_id}")
    #     # Call the camera hardware API
    #     # response = requests.get("http://CAMERA_API/capture")
    #     # image_path = save_image(response.content)  # save locally
    #     image_path = TEST_IMG_PATH
    #     detector = FaceDetector(KNOWN_STUDENTS_DIR)

    #     # Run face detection
    #     results = detector.detect_faces(image_path)

    #     # Save results to DB or return directly
    #     return {
    #         "class_id": class_id,
    #         "results": results,
    #         "status": "done"
    #     }

    # except Exception as e:
    #     return {"status": "failed", "error": str(e)}

