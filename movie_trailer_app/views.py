# movie_trailer_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from . import get_movie_trailer
import openai
import json
import requests

# Set up OpenAI credentials
openai.api_key = settings.OPENAI_API_KEY

def home(request):

    movies = []
    error_message = None
    if request.method == 'POST':
        model="gpt-3.5-turbo"
        text_input = request.POST.get('text_input')
        
        prompt = f"""
        I want you to recomend me 5 (five) movies that are similar in theme and genre to the 
        input movie.

        I need your awnser to be ONLY a ONE LINE list of the movie names separated by ```,``` 
        with no additional text or description.

        awnser format in case the input is correct: ```movie_1,movie_2,movie_3,movie_4,movie_5```

        awnser format in case the input doesnt correspond to a movie or tv show: ```None``` 

        MAKE SURE TO CHECK FOR GRAMMAR MISTAKES, IN CASE YOU CAN INTERPRET THE MOVIE WRITEN IN A DIFFERENT WAY USE THE AWNSER FOR THE CORRET INPUT

        input movie: ```{text_input}```
        """

        messages = [{"role": "user", "content": prompt}]
        # chama a api
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # Grau de Aleatoriedade
            
        )

        gpt_response = response.choices[0].message["content"]

        recom_m = gpt_response.split(',')

        print(recom_m)
        if recom_m[0] == 'None':
            error_message = "Insira um Filme Valido!"
        else:
            for title in recom_m:
                movie = {}

                movie['title'] = title
                movie['trailer_url'] = get_movie_trailer.get_movie_trailer(title)
                movie['description'] = title
                print(movie)
                movies.append(movie)
        
    
    
    context = {
        'movies': movies,
        'error_message': error_message,
    }
    


    return render(request, 'movie_trailer_app/index.html', context)

def get_gpt_response(request):
    if request.method == 'POST':
        model="gpt-3.5-turbo"
        user_msg = request.POST.get('messages')
        
        prompt = f"""
        I want you to recomend me 5 (five) movies that are similar in theme and genre to the 
        input movie.

        I need your awnser to be ONLY a ONE LINE list of the movie names separated by ```,``` 
        with no additional text or description.

        awnser format: ```movie_1, movie_2, movie_3, movie_4, movie_5``` 

        input movie: ```{user_msg}```
        """

        messages = [{"role": "user", "content": prompt}]
        # chama a api
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0, # Grau de Aleatoriedade
            
        )

        sent_response = response.choices[0].message["content"]
        # print(chat_response)
        # resposta em json JSON
        return JsonResponse({'chat_response': sent_response})
    else:
        return JsonResponse({'error': 'Invalid request method.'})