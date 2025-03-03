from flask import Flask
from flask.templating import render_template
from pony.orm import db_session

import db

app = Flask(__name__)

app.wsgi_app = db.db_session(app.wsgi_app)

db.operations.create_countries()


@app.route("/")
def hello():
    return render_template("index.html", name="World")


@db_session
@app.route("/<string:name>")
def hello_world(name: str):
    return render_template("index.html", name=name)
