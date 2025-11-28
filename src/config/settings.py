from dotenv import load_dotenv
import os

load_dotenv()

spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')
