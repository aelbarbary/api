# views.py
from django.http import JsonResponse
from rest_framework.views import APIView

from chatbot.platforms.docusaurus.scorer import Scorer  # Import the Scorer class

class ScoreView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract the document content from the request
        document_content = request.data.get('content', '')

        print("document_content",document_content)

        # Create an instance of the Scorer class
        scorer = Scorer(document_content)

        # Evaluate the document
        score = scorer.evaluate()

        response_data = {
            'score': score,
            'content': document_content
        }

        return JsonResponse(response_data)
