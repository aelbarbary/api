import json
import requests
import os

class VectaraQueryService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.vectara.io/v2/query"
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

    def query(self, query_text: str, corpus_key: str, metadata_filter: str = None, limit: int = 10, stream_response: bool = False):
        payload = {
            "query": query_text,
            "search": {
                "corpora": [
                    {
                        "custom_dimensions": {},
                        "metadata_filter": metadata_filter or "",
                        "lexical_interpolation": 0.025,
                        "semantics": "default",
                        "corpus_key": corpus_key
                    }
                ],
                "offset": 0,
                "limit": limit,
            },
            "generation": {
                "generation_preset_name": "vectara-summary-ext-v1.2.0",
                "max_used_search_results": 5,
            },
            "stream_response": stream_response
        }
        response = requests.post(self.url, headers=self.headers, data=json.dumps(payload), stream=True)
        if response.status_code == 200:
            if stream_response:
                return self.handle_stream_response(response)
            else:
                return response.json()
        else:
            response.raise_for_status()

    def handle_stream_response(self, response):
        for chunk in response.iter_lines():
            if chunk:
                decoded_chunk = chunk.decode('utf-8').strip()
                if decoded_chunk.startswith("data:"):
                    try:
                        json_data = json.loads(decoded_chunk[len("data:"):].strip())
                        yield json_data.get("generation_chunk", "")
                    except json.JSONDecodeError:
                        print("Could not decode chunk into JSON")
        return

# Lambda handler function
def lambda_handler(event, context):
    try:
        # Extract the prompt from the request body
        body = json.loads(event['body'])
        prompt = body.get('prompt', '')

        if not prompt:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Prompt is required'})
            }

        # Initialize VectaraQueryService with the API key from environment variables
        api_key = os.environ['VECTARA_API_KEY']
        service = VectaraQueryService(api_key)

        # Create a generator to stream the response
        response_generator = service.query(query_text=prompt, corpus_key="test", stream_response=True)

        response_data = []
        response_generator = service.query(query_text=prompt, corpus_key="test", stream_response=True)

        for chunk in response_generator:
            response_data.append({"answer": chunk})

        return {
            'statusCode': 200,
            'body': json.dumps(response_data),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
