import os
import face_recognition
import numpy as np



class FaceDetector:
    def __init__(self, known_faces_dir: str):
        self.known_faces_dir = known_faces_dir
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """
        Loads known faces from the specified directory.
        Each image file should be named as <student_id>.jpg or <name>.jpg
        """
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(self.known_faces_dir, filename)
                image = face_recognition.load_image_file(path)
                encodings = face_recognition.face_encodings(image)

                if encodings:
                    encoding = encodings[0]
                    self.known_encodings.append(encoding)

                    name = os.path.splitext(filename)[0]
                    self.known_names.append(name)
                else:
                    print(f"[WARN] No faces found in {filename}, skipping.")

    def detect_faces(self, image_path: str):
        """
        Detects faces in the provided image and matches them with known faces.

        Returns:
            A list of matched names (student IDs or names).
        """
        unknown_image = face_recognition.load_image_file(image_path)
        unknown_encodings = face_recognition.face_encodings(unknown_image)

        present_students = []

        for unknown_encoding in unknown_encodings:
            results = face_recognition.compare_faces(self.known_encodings, unknown_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(self.known_encodings, unknown_encoding)

            if True in results:
                best_match_index = np.argmin(face_distances)
                matched_name = self.known_names[best_match_index]
                present_students.append(matched_name)

        return present_students
