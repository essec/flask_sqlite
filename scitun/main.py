from flask import Flask, render_template, url_for, redirect
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
    print(std_form.data)
    student = models.Student()
    std_form.populate_obj(student)
    models.db.session.add(student)
    models.db.session.commit()
    return redirect(url_for("student_index"))


@app.route("/students/<student_id>")
def student_view(student_id):
    student = models.Student.query.filter_by(student_id=student_id).first()
    return render_template("/student/view.html", student=student)
    # return f"student {student_id}"
