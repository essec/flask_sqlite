import datetime
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

# Base = sa.ext.declarative.declarative_base()

db = SQLAlchemy()
Base = db.Model


def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


student_scholarship = sa.Table(
    "student_scholarship",
    Base.metadata,
    sa.Column("student_id", sa.Integer, sa.ForeignKey("students.student_id")),
    sa.Column(
        "scholarship_id", sa.Integer, sa.ForeignKey("scholarships.scholarship_id")
    ),
)


class Student(Base):
    __tablename__ = "students"

    student_id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)

    email = sa.Column(sa.String, nullable=True)

    lecturer_id = sa.Column(sa.Integer, sa.ForeignKey("lecturers.lecturer_id"))

    scholarships = sa.orm.relationship(
        "Scholarship", secondary=student_scholarship, back_populates="students"
    )


class Lecturer(Base):
    __tablename__ = "lecturers"

    lecturer_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)

    email = sa.Column(sa.String, nullable=True)

    advisee = sa.orm.relationship(
        "Student", backref=sa.orm.backref("lecturers"), lazy="dynamic"
    )


class Scholarship(Base):
    __tablename__ = "scholarships"

    scholarship_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.String)

    public_date = sa.Column(sa.DateTime, default=datetime.datetime.now())
    close_date = sa.Column(sa.DateTime, default=datetime.datetime.now())

    students = sa.orm.relationship(
        "Student", secondary=student_scholarship, back_populates="scholarships"
    )
