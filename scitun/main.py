from flask import Flask
import pathlib

from flask_sqlalchemy import model
import models

current_dir = pathlib.Path(__file__)
sqldatapath = current_dir.parent/"../data"
if not sqldatapath.exists():
    sqldatapath.mkdir(parents=True, exist_ok=True)


app = Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqldatapath.resolve()}/scitun.db"
models.init_app(app)
db = models.db


@app.route("/")
def index():
    return "Hello World!"
