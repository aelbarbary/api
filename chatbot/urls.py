from django.urls import path
from chatbot.views import MarkdownConvertView, ScoreView
from chatbot.views import  Chatbot

urlpatterns = [
    path('v1/answer/', Chatbot.as_view(), name='hello_world'),
    path('v1/convert/', MarkdownConvertView.as_view(), name='markdown_convert'),

    path('v1/score/', ScoreView.as_view(), name='score_view'),
]
