


from detector import FaceDetector

image_path = "./reals_test.jpg"
detector = FaceDetector("students/")
# Run face detection
results = detector.detect_faces(image_path)

# Save results to DB or return directly
print( {
    "class_id": "s",
    "results": results,
    "status": "done"
})