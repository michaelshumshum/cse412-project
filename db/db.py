import datetime
import os

from pony import orm

database = orm.Database(
    provider="postgres",
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    port=os.getenv("DB_PORT"),
)


class Country(database.Entity):
    name = orm.PrimaryKey(str)

    # ONETOMANY
    artists = orm.Set("Artist")
    record_labels = orm.Set("RecordLabel")


class RecordLabel(database.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    country = orm.Required(Country)
    founded = orm.Optional(int)
    logo = orm.Optional(str)  # url to image

    # ONETOMANY
    songs = orm.Set("Song")
    albums = orm.Set("Album")


class Artist(database.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    country = orm.Required(Country)
    biography = orm.Optional(str)
    popularity = orm.Optional(float)
    birthday = orm.Optional(datetime.datetime)

    # MANYTOMANY
    songs = orm.Set("Song")
    albums = orm.Set("Album")

    # ONETOONE
    producer = orm.Optional("Producer")


class Writer(database.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)

    # MANYTOMANY
    songs = orm.Set("Song")


class Producer(database.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    artist = orm.Optional(Artist)  # some producers are also artists

    # MANYTOMANY
    songs = orm.Set("Song")


class Song(database.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    artists = orm.Set(Artist)
    duration = orm.Optional(int)
    release_date = orm.Optional(datetime.datetime)
    lyrics = orm.Optional(str)
    album = orm.Optional("Album")
    record_label = orm.Optional(RecordLabel)
    track_index = orm.Optional(int)
    writers = orm.Set(Writer)
    producers = orm.Set(Producer)

    bpm = orm.Optional(int)
    key = orm.Optional(str)

    # ONETOMANY
    music_videos = orm.Set("MusicVideo")


class Album(database.Entity):
    id = orm.PrimaryKey(int, auto=True)
    name = orm.Required(str)
    artist = orm.Set(Artist)
    release_date = orm.Optional(datetime.datetime)
    record_label = orm.Optional(RecordLabel)
    cover_art = orm.Optional(str)  # url to image
    type = orm.Optional(str)
    num_tracks = orm.Optional(int)

    # ONETOMANY
    songs = orm.Set(Song)


class MusicVideo(database.Entity):
    id = orm.PrimaryKey(int, auto=True)
    for_song = orm.Required(Song)
    name = orm.Required(str)
    release_date = orm.Optional(datetime.datetime)
    duration = orm.Optional(int)
    url = orm.Optional(str)  # url to video, probably youtube


database.generate_mapping(create_tables=True)
