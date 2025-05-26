from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID  # if using Postgres
import uuid
from datetime import datetime

db = SQLAlchemy()

# User is a professor
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    classes = db.relationship("Classe", backref="professor", lazy=True)

class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    group = db.Column(db.Integer, nullable=False)  
    professor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    totalStudents = db.Column(db.Integer, default=0)
    students = db.relationship("Student", backref="class_ref", lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("classe.id"), nullable=False)



class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True)    
    result = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(25), default="PENDING") # PENDING, STARTED, FAILED, FINISHED
    
    def __repr__(self):
        return f"<Task id={self.id} title={self.title}>"