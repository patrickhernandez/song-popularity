import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

def get_songs_embeddings(lyrics):
        all_embeddings = []
        model = SentenceTransformer('distiluse-base-multilingual-cased-v2', device='mps')
        model_dim = model.get_sentence_embedding_dimension()

        for verses in lyrics:
            verse_embeddings = model.encode(verses, batch_size=64)
            song_embeddings = np.mean(verse_embeddings, axis=0)
            all_embeddings.append(song_embeddings)

        return pd.DataFrame(all_embeddings, columns=[f'emb_{i}' for i in range(model_dim)])