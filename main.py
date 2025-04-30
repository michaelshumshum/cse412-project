from flask import Flask, abort, request
from flask.templating import render_template
from pony.orm import db_session
import psycopg2

import db
from db.db import Album, Artist, Song

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


@app.route("/songs")
@db_session
def get_songs():
    artist_name = request.args.get("artist")
    album_name = request.args.get("album")

    query = Song.select()

    if artist_name:
        artist = Artist.get(name=artist_name)
        if not artist:
            return abort(404)
        query = query.filter(lambda s: artist in s.artists)

    if album_name:
        album = Album.get(name=album_name)
        if not album:
            return abort(404)
        query = query.filter(lambda s: s.album is album)

    return [{**song.to_dict()} for song in list(query)]


@db_session
@app.route("/artists")
def get_artists():
    artists = [{**artist.to_dict()} for artist in Artist.select()]
    return artists
