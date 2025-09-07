from langchain_core.tools import tool
from typing import List, Optional
import pandas as pd

from .recommender import recommender
from .tmdb import search_tmdb
from .titles import search_titles

@tool
def get_recommendations(summary: str = None, 
                        genres: List[str] = None, 
                        actors: List[str] = None, 
                        directors: List[str] = None, 
                        additional_keywords: str = None) -> dict:
    """
    Return film recommendations based on user-provided criteria.

    This function generates film recommendations by analyzing the provided 
    combination of parameters such as summary, genres, actors, directors, 
    and additional keywords. The more specific the input, the more refined 
    the recommendations will be.

    Parameters:
    ----------
    summary : str, optional
        A brief description or summary of a movie or show. This helps narrow down 
        recommendations based on similar plot themes or storytelling style. 
        Default is None.

    genres : List[str], optional
        A list of movie genres (e.g., ['Action', 'Comedy', 'Drama']). Recommendations 
        will be filtered based on these genres. Default is None.

    actors : List[str], optional
        A list of actor names (e.g., ['Leonardo DiCaprio', 'Scarlett Johansson']). 
        The function will prioritize films featuring these actors. Default is None.

    directors : List[str], optional
        A list of director names (e.g., ['Christopher Nolan', 'Quentin Tarantino']). 
        The function will prioritize films directed by these individuals. Default is None.

    additional_keywords : str, optional
        Any additional keywords or phrases (e.g., 'space exploration', 'romantic comedy') 
        to further refine the recommendations. Default is None.
"""
    
    return recommender(summary, genres, actors, directors, additional_keywords)

@tool
def lookup_titles(title: Optional[str] = None, director: Optional[str] = None) -> dict:
    """Performs a search for a title in our catalogue based on either title or a director.

    Args:
        title (str): The title to look up
        director (str): The director to look up
    
    Returns:
        dict: A dictionary of relevant search results
    """

    return search_titles(title, director)

@tool
def get_movie_info(title: str) -> bool:
    """Retrieves film metadata for a specified movie title"""

    return search_tmdb(title)
