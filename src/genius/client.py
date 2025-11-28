import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
import requests
import re
import json
from src.config.settings import genius_access_token

class GeniusClient:
    """
    """

    def __init__(self):
        self.access_token = genius_access_token

    def get_genius_urls(self, tracks, artists):
        all_urls = []
        search_url = 'https://api.genius.com/search'
        headers = {'Authorization': f'Bearer {self.access_token}'}

        for track, artist in zip(tracks, artists):
            params = {'q': f'{track} {artist}'}
            response = requests.get(search_url, headers=headers, params=params).json()
            hits = response['response']['hits']
            url = hits[0]['result']['url']

            all_urls.append(url)

        return all_urls
    
    def get_genius_lyrics(self, urls):
        all_lyrics = []

        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div', class_=re.compile(r'^Lyrics__Container-sc'))
            
            text = ' '.join(div.get_text(separator=' ', strip=True) for div in divs)
            lyrics = re.split(r'\[[^\]]+\]', text[text.find('['):])
            verses = [verse.strip() for verse in lyrics if verse.strip()]

            all_lyrics.append(verses)
        
        return all_lyrics
    
    def get_songs_embeddings(self, lyrics):
        all_embeddings = []
        model = SentenceTransformer('distiluse-base-multilingual-cased-v2', device='mps')
        model_dim = model.get_sentence_embedding_dimension()

        for verses in lyrics:
            verse_embeddings = model.encode(verses, batch_size=64)
            song_embeddings = np.mean(verse_embeddings, axis=0)
            all_embeddings.append(song_embeddings)

        return pd.DataFrame(all_embeddings, columns=[f'emb_{i}' for i in range(model_dim)])