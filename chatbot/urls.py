from django.urls import path
from chatbot.views import MarkdownConvertView
from chatbot.views import  Chatbot

urlpatterns = [
    path('v1/answer/', Chatbot.as_view(), name='hello_world'),
    path('v1/convert/', MarkdownConvertView.as_view(), name='markdown_convert'),
]
