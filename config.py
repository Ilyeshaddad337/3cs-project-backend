import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


HARDWARE_IP = os.environ.get("HARDWARE_IP") or "http://192.168.76.93:5000"
KNOWN_STUDENTS_DIR= os.path.join(os.getcwd(),"model/students")
TEST_IMG_PATH= os.path.join(os.getcwd(),"model/reals_test.jpg")
OUTPUT_FOLDER= os.path.join(os.getcwd(),"model/")


