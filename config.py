import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
KNOWN_STUDENTS_DIR= os.path.join(os.getcwd(),"model/students")
TEST_IMG_PATH= os.path.join(os.getcwd(),"model/reals_test.jpg")


