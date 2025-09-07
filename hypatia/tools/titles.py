from .recommender import df
from fuzzywuzzy import process

def search_titles(title: str = None, director: str = None) -> dict:

    if title and director:
        raise ValueError("Only one of `title` or `director` may be provided")
    
    if title:
        df['working_col'] = df['Title']
    elif director:
        df['working_col'] = df['Directors'].apply(lambda x: ', '.join(x))

    titles = df['working_col'].unique().tolist()
    
    results = process.extract(title or director, titles, limit = 2)
    matched_titles = [result[0] for result in results][::-1]

    result_df = df[df['working_col'].isin(matched_titles)]

    return result_df[['Title', 'Year', 'Summary', 'Directors', 'Genres', 'Roles']].to_dict()
