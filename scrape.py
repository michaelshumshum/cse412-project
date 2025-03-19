import json
import os

import dotenv
import requests

dotenv.load_dotenv()

auth_token = (
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

# do stuff
