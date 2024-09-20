from django.urls import path
from .views import  Chatbot

urlpatterns = [
    path('v1/answer/', Chatbot.as_view(), name='hello_world'),
]
