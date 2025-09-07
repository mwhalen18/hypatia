import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import numpy as np
from typing import List
import pandas as pd
import ast

PLEX_DATA_PATH = "/app/data/plex-output.csv"#"/Users/matthewwhalen/Projects/hypatia/data/plex-output.csv" #os.environ['PLEX_DATA_PATH']

df = pd.read_csv(PLEX_DATA_PATH)

cols_to_eval = [
    "Collections",
    "Countries",
    "Directors",
    "Genres",
    "Producers",
    "Roles"
]

for col in cols_to_eval:
    df[col] = df[col].apply(ast.literal_eval)

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Summary'])
director_mlb = MultiLabelBinarizer()
actor_mlb = MultiLabelBinarizer()
genres_mlb = MultiLabelBinarizer()

director_matrix = director_mlb.fit_transform(df['Directors'])
actor_matrix = actor_mlb.fit_transform(df['Roles'])
genres_matrix = genres_mlb.fit_transform(df['Genres'])

feature_matrix = np.hstack([
    tfidf_matrix.toarray(),
    director_matrix,
    actor_matrix,
    genres_matrix
])

def recommender(summary: str = None, 
                        genres: List[str] = None, 
                        actors: List[str] = None, 
                        directors: List[str] = None, 
                        additional_keywords: str = None):
    """
    Return film recommendations based on combinations of inputs.

    Args:
        summary (str): An optional synopsis of a film
        genres (list): An optional list of genres
        actors (list): An optional list of actors
        directors (list): An optional list of directors
        additional_keywords: An optional string of additional keywords of themes to be added to the recommendation query
    
    Returns:
        list: A list of film titles.
    """
    if summary is None and additional_keywords is None:
        query = None
    else:
        query = (summary or '') + '  \n' + (additional_keywords or '')

    query_tfidf_matrix = np.zeros((1, tfidf_matrix.shape[1]))
    if query is not None:
        query_tfidf_matrix = tfidf.transform([query]).toarray()
    
    #Genres
    if genres:
        query_genres_matrix = genres_mlb.transform([genres])
    else:    
        query_genres_matrix = np.zeros((1, genres_matrix.shape[1]))
    #Actors
    if actors:
        query_actor_matrix = actor_mlb.transform([actors])
    else:
        query_actor_matrix = np.zeros((1, actor_matrix.shape[1]))
    #Directors
    if directors:
        query_director_matrix = director_mlb.transform([directors])
    else:
        query_director_matrix = np.zeros((1, director_matrix.shape[1]))

    query_feature_matrix = np.hstack([
        query_tfidf_matrix,
        query_director_matrix,
        query_actor_matrix,
        query_genres_matrix
    ])

    sim_scores = cosine_similarity(query_feature_matrix, feature_matrix).flatten()
    # return np.sort(sim_scores)[-5:][::-1]
    top_indices = sim_scores.argsort()[-6:][::-1]
    return df.iloc[top_indices][['Title', 'Summary', 'Directors', 'Roles']]

def titles(title) -> bool:
    """confirm whether a given title exists in the catalogue. Returns True or False"""
    titles = df['Title'].unique().tolist()

    return title in titles