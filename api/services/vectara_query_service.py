import requests
import json

class VectaraQueryService:
    def __init__(self, api_key: str):
        """
        Initialize the VectaraQueryService with an API key.
        """
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
        try:
            for chunk in response.iter_lines():
                if chunk:  
                    decoded_chunk = chunk.decode('utf-8').strip()
                    if decoded_chunk.startswith("data:"):
                        try:
                            json_data = json.loads(decoded_chunk[len("data:"):].strip())
                            yield json_data.get("generation_chunk", "")
                        except json.JSONDecodeError:
                            print("Could not decode chunk into JSON")
        except requests.exceptions.RequestException as e:
            print(f"Stream error: {e}")
            raise e


