import json
import os

import dotenv
import requests

dotenv.load_dotenv()

spotify_auth_token = (
    "Bearer "
    + json.loads(
        requests.post(
            f"https://accounts.spotify.com/api/token?grant_type=client_credentials&client_id={os.getenv('SPOTIFY_CLIENT_ID')}&client_secret={os.getenv('SPOTIFY_CLIENT_SECRET')}",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        ).content
    )["access_token"]
)

headers = {
    "Authorization": spotify_auth_token,
    "Content-Type": "application/json",
}


def get_artist_id(artist_name: str) -> str:
    response = requests.get(
        f"https://api.spotify.com/v1/search?q={artist_name}&type=artist",
        headers=headers,
    )
    return json.loads(response.content)["artists"]["items"][0]["id"]


def get_albums(artist_id: str) -> list:
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/albums",
        headers=headers,
    )
    return json.loads(response.content)["items"]


def get_album_tracks(album_id: str) -> list:
    response = requests.get(
        f"https://api.spotify.com/v1/albums/{album_id}/tracks",
        headers=headers,
    )
    return json.loads(response.content)["items"]
