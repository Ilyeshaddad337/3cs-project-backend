from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api
from models import Classe, Student

@api.route("/classes", methods=["GET"])
@jwt_required()
def get_classes():
    user_id = int(get_jwt_identity())
    classes = Classe.query.filter_by(professor_id=user_id).all()
    return jsonify([{"id": c.id, "name": c.name, "group": c.group, "totalStudents":c.totalStudents} for c in classes])

@api.route("/students", methods=["GET"])
@jwt_required()
def get_students():
    user_id = int(get_jwt_identity())
    class_id = request.args.get("class_id")

    if not class_id:
        return jsonify({"msg": "Missing class_id in query parameters"}), 400

    klass = Classe.query.filter_by(id=class_id, professor_id=user_id).first()
    if not klass:
        return jsonify({"msg": "Class not found or access denied"}), 404

    students = Student.query.filter_by(class_id=class_id).all()
    return jsonify([{"id": s.id, "name": s.name} for s in students])

