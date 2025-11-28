import pandas as pd
import requests
import json
import time

class ReccoBeatsClient:
    """
    """

    def __init__(self):
        self.base_url = 'https://api.reccobeats.com/v1'

    def get_main_features(self, spotify_ids):
        all_main = []

        for spotify_id in spotify_ids:
            main_url = f'{self.base_url}/track?ids={spotify_id}'
            main_features = requests.get(main_url).json()

            if not main_features.get('content'):
                continue
            main = main_features['content'][0]
            main['artists'] = [a['name'] for a in main['artists']]
            main['spotify_id'] = spotify_id
            main = {k: main[k] for k in ['trackTitle', 'artists', 'durationMs', 'spotify_id']}

            all_main.append(main)
            time.sleep(0.1)

        return pd.DataFrame(all_main)
    
    def get_audio_features(self, spotify_ids):
        all_audio = []

        for spotify_id in spotify_ids:
            audio_url = f'{self.base_url}/audio-features?ids={spotify_id}'
            audio_features = requests.get(audio_url).json()

            if not audio_features.get('content'):
                continue
            audio = audio_features['content'][0]
            audio = {k: audio[k] for k in ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 
                                           'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'valence']}
            
            all_audio.append(audio)
            time.sleep(0.1)

        return pd.DataFrame(all_audio)

    def get_combined_features(self, spotify_ids):
        main_df = self.get_main_features(spotify_ids)
        audio_df = self.get_audio_features(spotify_ids)

        combined_df = pd.concat([main_df, audio_df], axis=1)

        return combined_df
    