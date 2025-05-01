from flask import Flask, abort, request
from flask.templating import render_template
from pony.orm import db_session

import db
from db.db import Album, Artist, Country, Producer, RecordLabel, Song, Writer

app = Flask(__name__)
app.static_folder = "static"

app.wsgi_app = db.db_session(app.wsgi_app)

db.operations.create_countries()


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route("/")
def index():
    return render_template("home.html")


# methods for searching
@app.route("/search", methods=["GET"])
def search():
<<<<<<< HEAD
    if request.method == 'POST':
    
        keyword = request.form['keyword']
        filter_type = request.form['filter']
    #cursor.execute()    #where we use SQL script to query based on user's search
        if filter_type == 'artists':
            cursor.execute("SELECT * FROM artists WHERE name ILIKE %s", ('%' + keyword + '%',))
        elif filter_type == 'albums':
            cursor.execute("SELECT * FROM albums WHERE name ILIKE %s", ('%' + keyword + '%',))
        elif filter_type == 'songs':
            cursor.execute("SELECT * FROM songs WHERE name ILIKE %s", ('%' + keyword + '%',))
        else:
            return "Invalid filter type"
        results = cursor.fetchall()
        return render_template("search_request.html", results=results, filter = filter_type)
    return render_template("search.html")
=======
    return abort(400)


@app.route("/search/songs")
@db_session
def search_songs():
    name = request.args.get("name", type=str)
    artist_id = request.args.get("artist", type=int)
    artist_name = request.args.get("artist_name", type=str)
    producer_id = request.args.get("producer", type=int)
    producer_name = request.args.get("producer_name", type=str)
    writer_id = request.args.get("writer", type=int)
    writer_name = request.args.get("writer_name", type=str)
    album_id = request.args.get("album", type=int)
    album_name = request.args.get("album_name", type=str)
    record_label_id = request.args.get("record_label", type=int)
    record_label_name = request.args.get("record_label_name", type=str)
    genre = request.args.get("genre", type=str)
    key = request.args.get("key", type=str)
    bpm_eq = request.args.get("bpm_eq", type=int)
    bpm_gt = request.args.get("bpm_gt", type=int)
    bpm_lt = request.args.get("bpm_lt", type=int)
    duration_eq = request.args.get("duration_eq", type=int)
    duration_gt = request.args.get("duration_gt", type=int)
    duration_lt = request.args.get("duration_lt", type=int)
    release_year = request.args.get("release_year", type=int)

    query = Song.select()
    title_filters = []

    if name:
        query = query.filter(lambda s: name.lower() in s.name.lower())
        title_filters.append(f'"is named like "{name}"')

    if artist_id:
        artist = Artist.get(id=artist_id)
        if not artist:
            return abort(404)

        query = query.filter(lambda s: artist in s.artists)

        title_filters.append(f'by artist "{artist.name}"')
    elif artist_name:
        artist = Artist.get(name=artist_name)
        if not artist:
            return abort(404)

        query = query.filter(lambda s: artist in s.artists)

        title_filters.append(f'by artist "{artist.name}"')

    if producer_id:
        producer = Producer.get(id=producer_id)
        if not producer:
            return abort(404)

        query = query.filter(lambda s: producer in s.producers)

        title_filters.append(f'by producer "{producer.name}"')
    elif producer_name:
        producer = Producer.get(name=producer_name)
        if not producer:
            return abort(404)

        query = query.filter(lambda s: producer in s.producers)

        title_filters.append(f'by producer "{producer.name}"')

    if writer_id:
        writer = Writer.get(id=writer_id)
        if not writer:
            return abort(404)

        query = query.filter(lambda s: writer in s.writers)

        title_filters.append(f'by writer "{writer.name}"')
    elif writer_name:
        writer = Writer.get(name=writer_name)
        if not writer:
            return abort(404)

        query = query.filter(lambda s: writer in s.writers)

        title_filters.append(f'by writer "{writer.name}"')

    if album_id:
        album = Album.get(id=album_id)
        if not album:
            return abort(404)

        query = query.filter(lambda s: album is s.album)

        title_filters.append(f'from album "{album.name}"')
    elif album_name:
        album = Album.get(name=album_name)
        if not album:
            return abort(404)

        query = query.filter(lambda s: album is s.album)

        title_filters.append(f'from album "{album.name}"')

    if record_label_id:
        record_label = RecordLabel.get(id=record_label_id)
        if not record_label:
            return abort(404)

        query = query.filter(lambda s: record_label is s.record_label)

        title_filters.append(f'from record label "{record_label.name}"')
    elif record_label_name:
        record_label = RecordLabel.get(name=record_label_name)
        if not record_label:
            return abort(404)

        query = query.filter(lambda s: record_label is s.record_label)

        title_filters.append(f'from record label "{record_label.name}"')

    if genre:
        query = query.filter(lambda s: genre == s.genre)
        title_filters.append(f'with genre "{genre}"')

    if release_year:
        query = query.filter(lambda s: release_year == s.release_date.year)
        title_filters.append(f"released in {release_year}")

    if key:
        query = query.filter(lambda s: key == s.key)
        title_filters.append(f'with key "{key}"')

    if bpm_eq:
        query = query.filter(lambda s: s.bpm == bpm_eq)
        title_filters.append(f'with bpm "{bpm_eq}"')

    if bpm_gt:
        query = query.filter(lambda s: s.bpm > bpm_gt)
        title_filters.append(f'with bpm greater than "{bpm_gt}"')

    if bpm_lt:
        query = query.filter(lambda s: s.bpm < bpm_lt)
        title_filters.append(f'with bpm less than "{bpm_lt}"')

    if duration_eq:
        query = query.filter(lambda s: s.duration == duration_eq)
        title_filters.append(f'with duration "{duration_eq}"')

    if duration_gt:
        query = query.filter(lambda s: s.duration > duration_gt)
        title_filters.append(f'with duration greater than "{duration_gt}"')

    if duration_lt:
        query = query.filter(lambda s: s.duration < duration_lt)
        title_filters.append(f'with duration less than "{duration_lt}"')

    result = [
        {**song.to_dict(with_collections=True, related_objects=True)}
        for song in list(query)
    ]

    return render_template(
        "search_result.html", title=f"Songs {', '.join(title_filters)}", songs=result
    )


@app.route("/search/albums")
def search_albums():
    name = request.args.get("name", type=str)
    artist_id = request.args.get("artist", type=int)
    artist_name = request.args.get("artist_name", type=str)
    record_label_id = request.args.get("record_label", type=int)
    record_label_name = request.args.get("record_label_name", type=str)
    genre = request.args.get("genre", type=str)
    release_year = request.args.get("release_year", type=int)
    num_tracks_eq = request.args.get("num_tracks_eq", type=int)
    num_tracks_gt = request.args.get("num_tracks_gt", type=int)
    num_tracks_lt = request.args.get("num_tracks_lt", type=int)

    query = Album.select()
    title_filters = []

    if name:
        query = query.filter(lambda a: name.lower() in a.name.lower())
        title_filters.append(f'is named like "{name}"')

    if artist_id:
        artist = Artist.get(id=artist_id)
        if not artist:
            abort(404)
        query = query.filter(lambda a: artist in a.artist)
        title_filters.append(f'with artist "{artist.name}"')
    elif artist_name:
        artist = Artist.get(name=artist_name)
        if not artist:
            abort(404)
        query = query.filter(lambda a: artist in a.artist)
        title_filters.append(f'with artist "{artist.name}"')

    if record_label_id:
        record_label = RecordLabel.get(id=record_label_id)
        query = query.filter(lambda a: a.record_label == record_label)
        title_filters.append(f'from record label "{record_label.name}"')
    elif record_label_name:
        record_label = RecordLabel.get(name=record_label_name)
        if not record_label:
            abort(404)
        query = query.filter(lambda a: record_label == a.record_label)
        title_filters.append(f'from record label "{record_label.name}"')

    if release_year:
        query = query.filter(lambda a: release_year == a.release_date.year)
        title_filters.append(f"released in {release_year}")

    if genre:
        query = query.filter(lambda a: genre == a.genre)
        title_filters.append(f'with genre "{genre}"')

    if num_tracks_eq:
        query = query.filter(lambda a: a.num_tracks == num_tracks_eq)
        title_filters.append(f"with {num_tracks_eq} tracks")

    if num_tracks_gt:
        query = query.filter(lambda a: a.num_tracks > num_tracks_gt)
        title_filters.append(f"with more than {num_tracks_gt} tracks")

    if num_tracks_lt:
        query = query.filter(lambda a: a.num_tracks < num_tracks_lt)
        title_filters.append(f"with less than {num_tracks_lt} tracks")

    result = [
        {**album.to_dict(with_collections=True, related_objects=True)}
        for album in list(query)
    ]

    return render_template(
        "search_result.html", title=f"Albums {', '.join(title_filters)}", albums=result
    )


@app.route("/search/artists")
def search_artists():
    name = request.args.get("name", type=str)
    country = request.args.get("country", type=str)
    birth_year = request.args.get("birth_year", type=int)
    popularity_eq = request.args.get("popularity_eq", type=int)
    popularity_gt = request.args.get("popularity_gt", type=int)
    popularity_lt = request.args.get("popularity_lt", type=int)

    query = Artist.select()
    title_filters = []

    if name:
        query = query.filter(lambda a: a.name.startswith(name))

        title_filters.append(f"named like {name}")

    if birth_year:
        query = query.filter(lambda a: a.birthday.year == birth_year)

        title_filters.append(f"born in {birth_year}")

    if country:
        country_object = Country.get(name=country)
        if not country_object:
            return abort(404)
        query = query.filter(lambda a: a.country is country_object)

        title_filters.append(f"from {country_object.name}")

    if popularity_eq:
        query = query.filter(lambda a: a.popularity == popularity_eq)

        title_filters.append(f"with popularity = {popularity_eq}")

    if popularity_gt:
        query = query.filter(lambda a: a.popularity > popularity_gt)

        title_filters.append(f"with popularity > {popularity_gt}")

    if popularity_lt:
        query = query.filter(lambda a: a.popularity < popularity_lt)

        title_filters.append(f"with popularity < {popularity_lt}")

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
>>>>>>> a8f8aa8e8ebcc2cbe7abd62c8a134496adf1d598


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
