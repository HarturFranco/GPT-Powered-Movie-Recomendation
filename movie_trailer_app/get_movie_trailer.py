import requests
from django.conf import settings

def get_movie_trailer(movie_name):
    base_url = 'https://api.themoviedb.org/3'
    api_key = settings.TMDB_API_KEY

    # Search for the movie
    search_url = f'{base_url}/search/movie'
    search_params = {
        'api_key': api_key,
        'query': movie_name
    }
    response = requests.get(search_url, params=search_params)
    data = response.json()

    # Check if any results found
    if data['total_results'] > 0:
        movie_id = data['results'][0]['id']

        # Get the movie details
        movie_url = f'{base_url}/movie/{movie_id}/videos'
        movie_params = {
            'api_key': api_key
        }
        response = requests.get(movie_url, params=movie_params)
        data = response.json()

        # Check if any trailers found
        if data['results']:
            trailer_key = data['results'][0]['key']
            trailer_url = f'https://www.youtube.com/embed/{trailer_key}'

            return trailer_url

    return None


# print(get_movie_trailer("memento"))