# converter/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os

from api.utils.MarkdownToVectaraConverter import MarkdownToVectaraConverter


class MarkdownConvertView(APIView):

    def post(self, request, format=None):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file_obj = request.FILES['file']
        filename = file_obj.name
        
        # Save the file temporarily
        with open(filename, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        converter = MarkdownToVectaraConverter(filename)
        vectara_json = converter.convert()

        os.remove(filename)  # Clean up the file after processing
        return Response(vectara_json, status=status.HTTP_200_OK)
