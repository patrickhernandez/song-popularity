from src.spotify.client import SpotifyClient
from src.reccobeats.client import ReccoBeatsClient
from src.kworb.client import KworbClient
from src.genius.client import GeniusClient
from src.utils.dates import get_dates
import pandas as pd

spotify = SpotifyClient()
reccobeats = ReccoBeatsClient()
kworb = KworbClient()
genius = GeniusClient()

query_list = kworb.get_top_artists(2500)
dates = get_dates('2017-06-28', '2025-12-01')

spotify_ids = spotify.get_track_ids(query_list, filter='after', year=2017)
track_df = reccobeats.get_combined_features(spotify_ids)
# clean track_df: get rid of duplicates

full_charts_df = kworb.get_apple_music_charts(dates)
unique_charts_df = kworb.get_unique_apple_music(full_charts_df)
# add popular column using unique_charts_df

genius_urls = genius.get_genius_urls(track_df['trackTitle'], track_df['artists'])
genius_lyrics = genius.get_genius_lyrics(genius_urls)
embeddings_df = genius.get_songs_embeddings(genius_lyrics)
# concat embeddings_df to track_df
