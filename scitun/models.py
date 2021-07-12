import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

Base = sa.ext.declarative.declarative_base()

db = SQLAlchemy()
# Base = db.Model


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


class Student(Base):
    __tablename__ = "students"

    student_id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)

    email = sa.Column(sa.String, nullable=True)

    lecturer_id = sa.Column(sa.Integer, sa.ForeignKey("lecturers.lecturer_id"))


class Lecturer(Base):
    __tablename__ = "lecturers"

    lecturer_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)

    email = sa.Column(sa.String, nullable=True)

    advisee = sa.orm.relationship(
        "Student", backref=sa.orm.backref("lecturers"), lazy="dynamic"
    )
