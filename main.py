from flask import Flask, abort, request
from flask.templating import render_template
from pony.orm import db_session

import db
from db.db import Album, Artist, Song

app = Flask(__name__)

app.wsgi_app = db.db_session(app.wsgi_app)

db.operations.create_countries()


@app.route("/")
def index():
    return render_template("home.html")


# method for searching
@app.route("/search", methods=["GET"])
def search():
    return render_template("search_request.html")


@app.route("/songs")
@db_session
def get_songs():
    query = Song.select()

    artist_names = request.args.get("artist")
    if artist_names:
        artists = [
            Artist.get(name=artist_name) for artist_name in artist_names.split(",")
        ]
        if not all(artists):
            return abort(404)

        queries = []
        for artist in artists:
            queries.append(query.filter(lambda a: artist in a.artists))
        query = queries[0]
        for q in queries[1:]:
            query = query.union(q)

    album_name = request.args.get("album")
    if album_name:
        album = Album.get(name=album_name)
        if not album:
            return abort(404)
        query = query.filter(lambda s: s.album is album)

    result = [
        {**song.to_dict(with_collections=True, related_objects=True)}
        for song in list(query.distinct())
    ]

    # serialize the nested collections
    for song in result:
        a_l = []
        for artist in song["artists"]:
            d = {
                "id": artist.id,
                "name": artist.name,
            }
            a_l.append(d)
        song["artists"] = a_l

        p_l = []
        for producer in song["producers"]:
            d = {
                "id": producer.id,
                "name": producer.name,
            }
            p_l.append(d)
        song["producers"] = p_l

        w_l = []
        for writer in song["writers"]:
            d = {
                "id": writer.id,
                "name": writer.name,
            }
            w_l.append(d)
        song["writers"] = w_l

        m_l = []
        for music_video in song["music_videos"]:
            d = {
                "id": music_video.id,
                "name": music_video.name,
            }
            m_l.append(d)
        song["music_videos"] = m_l

        song["album"] = {
            "id": song["album"].id,
            "name": song["album"].name,
        }

        song["record_label"] = {
            "id": song["record_label"].id,
            "name": song["record_label"].name,
        }

        print(song)

    return result


@db_session
@app.route("/artists")
def get_artists():
    query = Artist.select()

    country_name = request.args.get("country")
    if country_name:
        query = query.filter(lambda a: a.country == country_name)

    return [{**artist.to_dict()} for artist in list(query)]


@app.route("/albums")
@db_session
def get_albums():
    artist_names = request.args.get("artist")

    query = Album.select()

    if artist_names:
        artists = [
            Artist.get(name=artist_name) for artist_name in artist_names.split(",")
        ]
        if not all(artists):
            return abort(404)
        query.filter(lambda a: a)

    return [{**album.to_dict()} for album in list(query.distinct())]
