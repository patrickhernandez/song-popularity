import pandas as pd
from bs4 import BeautifulSoup
import requests

class KworbClient:
    """
    """

    def __init__(self):
        self.base_url = 'https://kworb.net'

    def get_top_artists(self, n):
        all_artists = []

        artists_url = f'{self.base_url}/itunes/extended.html'
        response = requests.get(artists_url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')

        for row in table.find_all('tr')[1:]:
            artist = row.find_all('td')[1].find('a').get_text(strip=True)
            all_artists.append(artist)

            if len(all_artists) >= n:
                break

        return all_artists
    
    def get_apple_music_charts(self, dates):
        all_charts = []

        for date in dates:
            date_string = date.strftime('%Y%m%d')
            chart_url = f'{self.base_url}/apple_songs/archive/{date_string}.html'
            response = requests.get(chart_url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')

            for row in table.find_all('tr')[1:]:
                cols = row.find_all('td')
                rank = int(cols[0].get_text(strip=True))
                try:
                    artists, title = cols[2].find('div').get_text(strip=True).rsplit(' - ', 1)
                except ValueError:
                    continue
                artists = [artist.strip() for artist in artists.split('&')]

                all_charts.append({'trackTitle': title, 'artists': artists, 'date': date, 'rank': rank})

        return pd.DataFrame(all_charts)
    
    def get_unique_apple_music(self, charts_df):
        charts_df['artists'] = charts_df['artists'].apply(tuple)
        charts_df = charts_df.sort_values(['trackTitle', 'artists', 'rank', 'date'])
        
        unique_charts_df = charts_df.groupby(['trackTitle', 'artists'], as_index=False).first()
        unique_charts_df['artists'] = unique_charts_df['artists'].apply(list)
        unique_charts_df = unique_charts_df.rename(columns={'date': 'best_date', 'rank': 'best_rank'})

        return unique_charts_df
        