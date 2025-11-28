import requests
import json
import time
from src.config.settings import spotify_client_id, spotify_client_secret

class SpotifyClient:
    """
    """

    def __init__(self):
        self.client_id = spotify_client_id
        self.client_secret = spotify_client_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        data = {'grant_type': 'client_credentials', 'client_id': self.client_id, 'client_secret': self.client_secret}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(token_url, data=data, headers=headers)
        
        return response.json()['access_token']
    
    def get_track_ids(self, query_list, filter=None, year=None):
        track_ids = []
        headers = {'Authorization': f'Bearer {self.access_token}'}

        for query in query_list:
            search_url = f'https://api.spotify.com/v1/search?q={query}&type=track&limit=50'
            response = requests.get(search_url, headers=headers)
            tracks = response.json().get('tracks', {}).get('items', [])

            for track in tracks:
                release_year = int(track['album']['release_date'].split('-')[0])
                if filter and year:
                    if filter == 'before' and release_year >= year:
                        continue
                    elif filter == 'after' and release_year < year:
                        continue
                track_ids.append(track['id'])

            time.sleep(0.1)
        
        return track_ids
    