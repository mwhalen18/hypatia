from themoviedb import TMDb
import os

tmdb = TMDb(key = os.environ["TMDB_API_KEY"])


def search_tmdb(title: str):
    movies = tmdb.search().movies(title, include_adult=True)

    try:
        movie_id = movies[0].id
    except:
        return "Could not find a title by that name"

    movie = tmdb.movie(movie_id).details(append_to_response="credits")

    out = {
        'Title': movie.title,
        'Summary': movie.overview,
        'Director(s)': [person.name for person in movie.credits.crew if person.job == 'Director'],
        'Genre(s)': [genre.name for genre in movie.genres],
        'Roles': [person.name for person in movie.credits.cast][0:5]
    }

    return out