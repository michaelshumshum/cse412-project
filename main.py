from flask import Flask, request
from flask.templating import render_template
from pony.orm import db_session
import psycopg2

import db

app = Flask(__name__)

app.wsgi_app = db.db_session(app.wsgi_app)

db.operations.create_countries()

#added connection in main,
#to store keywords collected from user when interacting with site
conn = psycopg2.connect(
    dbname = 'testname',
    user = 'testuser',
    password = 'testpassword',
    host = 'localhost'
)

cursor = conn.cursor()

@app.route("/")
def hello():
    return render_template("index.html", name="World")

#method for searching
@app.route("/search", methods = ['POST'])
def search():
    keyword = request.form['keyword']
    cursor.execute()    #where we use SQL script to query based on user's search
    results = cursor.fetchall()
    return render_template("search_request.html", results=results)


@db_session
@app.route("/<string:name>")
def hello_world(name: str):
    return render_template("index.html", name=name)
