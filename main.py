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


# methods for searching
@app.route("/search", methods=["GET"])
def search():
    return render_template("search_request.html")


@app.route("/search/songs")
@db_session
def search_artist_by_id():
    artist_id = request.args.get("artist", type=int)
    album_id = request.args.get("album", type=int)
    genre = request.args.get("genre", type=str)

    query = Song.select()
    title_filters = []

    if artist_id:
        artist = Artist.get(id=artist_id)
        if not artist:
            return abort(404)

        query = query.filter(lambda s: artist in s.artists)

        title_filters.append(f'by artist "{artist.name}"')

    if album_id:
        album = Album.get(id=album_id)
        if not album:
            return abort(404)

        query = query.filter(lambda s: album is s.album)

        title_filters.append(f'from album "{album.name}"')

    if genre:
        query = query.filter(lambda s: genre == s.genre)
        title_filters.append(f'with genre "{genre}"')

    result = [
        {**song.to_dict(with_collections=True, related_objects=True)}
        for song in list(query)
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

    return render_template(
        "search_result.html", title=f"Songs {', '.join(title_filters)}", songs=result
    )


@app.route("/search/artists")
def search_artists():
    name = request.args.get("name")
    country = request.args.get("country")

    query = Artist.select()
    title_filters = []

    if name:
        query = query.filter(lambda a: a.name.startswith(name))

    if country:
        query = query.filter(lambda a: a.country == country)

    result = [
        {**artist.to_dict(with_collections=True, related_objects=True)}
        for artist in list(query.distinct())
    ]

    return render_template(
        "search_result.html",
        title=f"Artists {', '.join(title_filters)}",
        artists=result,
    )


# regular getting


@app.route("/songs")
@db_session
def get_songs():
    query = Song.select()

    artist_name = request.args.get("artist")
    if artist_name:
        artist = Artist.get(name=artist_name)
        if not artist:
            return abort(404)
        query = query.filter(lambda s: artist in s.artists)

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
    artist_name = request.args.get("artist")

    query = Album.select()

    if artist_name:
        artist = Artist.get(name=artist_name)
        if not artist:
            return abort(404)
        query.filter(lambda a: artist in a.artist)

    result = [
        {**album.to_dict(with_collections=True, related_objects=True)}
        for album in list(query.distinct())
    ]

    for album in result:
        a_l = []
        for artist in album["artist"]:
            d = {
                "id": artist.id,
                "name": artist.name,
            }
            a_l.append(d)
        del album["artist"]
        album["artists"] = a_l

        album["record_label"] = {
            "id": album["record_label"].id,
            "name": album["record_label"].name,
        }

        del album["songs"]

    return result
