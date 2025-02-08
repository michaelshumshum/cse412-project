from flask import Flask
from flask.templating import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html", name="World")


@app.route("/<string:name>")
def hello_world(name: str):
    return render_template("index.html", name=name)
