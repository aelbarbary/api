import json
from django.http import StreamingHttpResponse
from django.shortcuts import render
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
import environ
import requests
from api.services.vectara_query_service import VectaraQueryService
env = environ.Env()


class Chatbot(APIView):
    def __init__(self):
        api_key = env('VECTARA_API_KEY')
        self.service = VectaraQueryService(api_key)
    
    def stream_response(self, prompt):
        for chunk in self.service.query(
                query_text=prompt,
                corpus_key="test",
                stream_response=True
            ):
            if chunk:  # Check if chunk is not empty
                yield json.dumps({"answer": chunk}) + "\n"

    def post(self, request):
        prompt = request.data.get('prompt', '')
        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = StreamingHttpResponse(self.stream_response(prompt), content_type='application/json')
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
   