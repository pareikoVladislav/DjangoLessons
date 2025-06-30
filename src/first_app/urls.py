from django.urls import path

from src.first_app.views import greetings

urlpatterns = [
    path('', greetings),
]
