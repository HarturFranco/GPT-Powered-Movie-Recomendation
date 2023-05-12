from django.urls import path

from .views import home, get_gpt_response

urlpatterns = [
    path("", home, name="home"),
    path('get_gpt_response/', get_gpt_response, name='get_gpt_response'),
]