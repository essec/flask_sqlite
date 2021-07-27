from flask import Flask, render_template, url_for, redirect, request
import pathlib

from flask_sqlalchemy import model
import models
import forms

current_dir = pathlib.Path(__file__)
sqldatapath = current_dir.parent / "../data"
if not sqldatapath.exists():
    sqldatapath.mkdir(parents=True, exist_ok=True)


app = Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqldatapath.resolve()}/scitun.db"


@app.before_first_request
def init_flask():
    models.init_app(app)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/students")
def student_index():
    students = models.Student.query.all()
    return render_template("/student/index.html", students=students)


@app.route("/students/register", methods=["GET", "POST"])
def register_student():
    std_form = forms.Student()
    if not std_form.validate_on_submit():
        print(std_form.errors)
        return render_template("student/register.html", std_form=std_form)
    # print(std_form.data)
    student = models.Student()
    std_form.populate_obj(student)
    models.db.session.add(student)
    models.db.session.commit()
    return redirect(url_for("student_index"))


@app.route("/students/<student_id>")
def student_view(student_id):
    student = models.Student.query.filter_by(student_id=student_id).first()
    return render_template("/student/view.html", student=student)


@app.route("/lecturers")
def lecturer_index():
    lecturers = models.Lecturer.query.all()
    return render_template("/lecturer/index.html", lecturers=lecturers)


@app.route("/lecturers/register", methods=["GET", "POST"])
def register_lecturer():
    form = forms.Lecturer()
    if not form.validate_on_submit():
        print(form.errors)
        return render_template("lecturer/register.html", form=form)
    # print(form.data)
    lecturer = models.Lecturer()
    form.populate_obj(lecturer)
    models.db.session.add(lecturer)
    models.db.session.commit()
    return redirect(url_for("lecturer_index"))


@app.route("/lecturers/<lecturer_id>")
def lecturer_view(lecturer_id):
    lecturer = models.Lecturer.query.filter_by(lecturer_id=lecturer_id).first()
    students = models.Student.query.filter_by(lecturer_id=None).all()
    form = forms.AssignStudent()
    form.student.choices = [
        (student.student_id, student.student_id) for student in students
    ]
    if not form.validate_on_submit():
        return render_template("/lecturer/view.html", lecturer=lecturer, form=form)
    return redirect(url_for("lecturer_view", lecturer_id=lecturer.lecturer_id))


@app.route("/advicer/register", methods=["POST"])
def assign_student():
    student_id = request.form.get("student")
    lecturer_id = request.form.get("lecturer_id")
    student = models.Student.query.filter_by(student_id=student_id).first()
    lecturer = models.Lecturer.query.filter_by(lecturer_id=lecturer_id).first()
    if lecturer and student:
        lecturer.advisee.append(student)
    models.db.session.commit()
    return redirect(url_for("lecturer_view", lecturer_id=lecturer_id))


@app.route("/scholarships")
def scholarships_index():
    scholarships = models.Scholarship.query.all()
    return render_template("/scholarships/index.html", scholarships=scholarships)


@app.route("/scholarships/create", methods=["GET", "POST"])
def create_scholarship():
    form = forms.Scholarship()
    if not form.validate_on_submit():
        print(form.errors)
        return render_template("/scholarships/create.html", form=form)
    scholarship = models.Scholarship()
    form.populate_obj(scholarship)
    models.db.session.add(scholarship)
    models.db.session.commit()
    return redirect(url_for("scholarships_index"))


@app.route("/scholarships/<scholarship_id>")
def scholarship_view(scholarship_id):
    form = forms.AssignStudent()
    students = models.Student.query.all()
    form.student.choices = [
        (student.student_id, student.student_id) for student in students
    ]
    scholarship = models.Scholarship.query.filter_by(
        scholarship_id=scholarship_id
    ).first()
    if not form.validate_on_submit():
        return render_template(
            "/scholarships/view.html", scholarship=scholarship, form=form
        )
    return redirect(
        url_for("scholarship_view", scholarship_id=scholarship.scholarship_id)
    )


@app.route("/scholarships/assign_student", methods=["POST"])
def scholarship_assign_student():
    student_id = request.form.get("student")
    scholarship_id = request.form.get("scholarship_id")
    student = models.Student.query.filter_by(student_id=student_id).first()
    scholarship = models.Scholarship.query.filter_by(scholarship_id=scholarship_id).first()
    if (scholarship and student) and student not in scholarship.students:
        scholarship.students.append(student)
        models.db.session.commit()
    return redirect(url_for("scholarship_view", scholarship_id=scholarship_id))
