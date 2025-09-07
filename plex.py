from plexapi.myplex import MyPlexAccount
import pandas as pd
from tqdm import tqdm
import logging

def scrape():
    try:
        account = MyPlexAccount('matthewwhalen544', '*9a&%&gh&G@58GMwMT')
        plex = account.resource('cleopatra').connect()
    except:
        raise Exception("Could not connect to plex")
    
    try:
        movies = plex.library.section('Movies')

        all_movies = movies.all()
        movie_data = []

        for movie in tqdm(all_movies):
            movie_info = {
                'Title': movie.title,
                'Year': movie.year,
                'Rating': movie.rating,
                'Studio': movie.studio,
                'Summary': movie.summary,
                'Content Rating': movie.contentRating,
                'Collections': [collection.tag for collection in movie.collections],
                'Countries': [country.tag for country in movie.countries],
                'Directors': [director.tag for director in movie.directors],
                'Genres': [genre.tag for genre in movie.genres],
                'Producers': [producer.tag for producer in movie.producers],
                'Roles': [role.tag for role in movie.roles],
            }
            movie_data.append(movie_info)

        df = pd.DataFrame(movie_data)
        list_cols = ['Countries', 'Directors', 'Genres', 'Producers', 'Roles']

        for col in list_cols:
            df[col] = df[col].apply(lambda x: x[0:5] if isinstance(x, list) else x)

        df.to_csv("data/plex-output.csv", index = False)
    
    except Exception as e:
        raise ValueError(str(e))