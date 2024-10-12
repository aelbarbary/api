from django.urls import path
from api.views import MarkdownConvertView
from api.views import  Chatbot

urlpatterns = [
    path('v1/answer/', Chatbot.as_view(), name='hello_world'),
    path('v1/convert/', MarkdownConvertView.as_view(), name='markdown_convert'),
]
