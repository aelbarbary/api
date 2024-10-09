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
from api.services.vectara_query_service import VectaraQueryBuilder, VectaraQueryService
env = environ.Env()


class Chatbot(APIView):
    def __init__(self):
        api_key = env('VECTARA_API_KEY')
        self.service = VectaraQueryService(api_key=api_key)
        
    def stream_response(self, prompt, query_params):
        query_builder = VectaraQueryBuilder(query_text=prompt, corpus_key="test")

        for key, value in query_params.items():
            if key == "limit":
                query_builder.set_limit(value)
            elif key == "metadata_filter":
                query_builder.set_metadata_filter(value)
            elif key == "lexical_interpolation":
                query_builder.set_lexical_interpolation(value)
            
        for chunk in self.service.query(query_builder):
            if chunk: 
                yield json.dumps({"answer": chunk}) + "\n"

    def post(self, request):
        prompt = request.data.get('prompt', '')
        query_params = request.data.get('query_params', {}) 
        if not prompt:
            return Response({'error': 'Prompt is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            response = StreamingHttpResponse(self.stream_response(prompt, query_params), content_type='application/json')
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
   