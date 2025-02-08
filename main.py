import atexit

from flask import Flask
from flask.templating import render_template

import db

app = Flask(__name__)

db.create_tables()


def cleanup():
    db.cleanup()


@app.route("/")
def hello():
    return render_template("index.html", name="World")


@app.route("/<string:name>")
def hello_world(name: str):
    return render_template("index.html", name=name)


atexit.register(cleanup)
