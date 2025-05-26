from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db
from routes import api
from werkzeug.security import generate_password_hash





def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app)
    jwt = JWTManager(app)
    
    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        return str(user_id)

    return app




app = create_app()

if __name__ == "__main__":
    app.register_blueprint(api)
    
    with app.app_context():
        db.create_all()

        # Create demo professor and data if not exists
        from models import User, Classe, Student

        if not User.query.first():
            prof = User(username="a.rahmoune@esi-sba.dz",name="Rahmoune", password=generate_password_hash("password"))
            db.session.add(prof)
            db.session.commit()

            c1 = Classe(name="ISI", group="G01", totalStudents=20, professor_id=prof.id)
            c2 = Classe(name="ISI", group="G02", totalStudents=20, professor_id=prof.id)
            db.session.add_all([c1, c2])
            db.session.commit()

            students = [
                Student(name="haddad ilyes", class_id=c1.id),
                Student(name="omri ilyes", class_id=c1.id),
                Student(name="fendi mohammed", class_id=c2.id),
            ]
            db.session.add_all(students)
            db.session.commit()
            print("✔️ Demo data added")

    app.run(debug=True)
