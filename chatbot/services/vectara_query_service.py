import requests
import json
from typing import List, Tuple


class VectaraQueryBuilder:
    def __init__(self, query_text: str, corpus_key: str):
        self.payload = {
            "query": query_text,
            "search": {
                "corpora": [
                    {
                        "custom_dimensions": {},
                        "metadata_filter": "",
                        "lexical_interpolation": 0.025,
                        "semantics": "default",
                        "corpus_key": corpus_key
                    }
                ],
                "offset": 0,
                "limit": 10, 
            },
            "generation": {
                "prompt_name": "mockingbird-1.0-2024-07-16",
                "max_used_search_results": 5
            },
            "stream_response": True
        }

    def set_limit(self, limit: int):
        self.payload['search']['limit'] = limit
        return self

    def set_metadata_filter(self, metadata_filter: str):
        self.payload['search']['corpora'][0]['metadata_filter'] = metadata_filter
        return self

    def set_lexical_interpolation(self, lexical_interpolation: str):
        self.payload['search']['corpora'][0]['lexical_interpolation'] = lexical_interpolation
        return self

    def set_stream_response(self, stream_response: bool):
        self.payload['stream_response'] = stream_response
        return self

    def set_prompt_name(self, prompt_name: str):
        self.payload['generation']['prompt_name'] = prompt_name
        return self

    def build(self):
        return self.payload



class VectaraQueryService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.vectara.io/v2/query"
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        
    def query(self, builder: VectaraQueryBuilder):
        payload = builder.build()
        print(payload)
        response = requests.post(self.url, headers=self.headers, data=json.dumps(payload), stream=True)
        if response.status_code == 200:
            if payload.get("stream_response", False):
                return self.handle_stream_response(response) 
            else:
                return response.json()  
        else:
            response.raise_for_status() 
    
    def extract_sorted_urls(self, data: List[dict]) -> List[str]:
        url_scores = {}
        for item in data[:3]:
            if 'documentation_url' in item['document_metadata']:
                url = item['document_metadata']['documentation_url']
                score = item['score']
                if url not in url_scores or score > url_scores[url]:
                    url_scores[url] = score

            if 'url' in item['part_metadata']:
                url = item['part_metadata']['url']
                score = item['score']
                if url not in url_scores or score > url_scores[url]:
                    url_scores[url] = score

        sorted_urls = sorted(
            ((url, score) for url, score in url_scores.items()),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [url for url, score in sorted_urls]



    def handle_stream_response(self, response):
        try:
            all_urls = []
            for chunk in response.iter_lines():

                if chunk:  
                    decoded_chunk = chunk.decode('utf-8').strip()
                    
                    if decoded_chunk.startswith("data:"):
                        try:
                            
                            json_data = json.loads(decoded_chunk[len("data:"):].strip())
                            if json_data.get("type") == "search_results":
                                urls = self.extract_sorted_urls(json_data.get("search_results", []))
                                all_urls.extend(urls)  # Accumulate URLs

                            yield json_data.get("generation_chunk", "")
                        except json.JSONDecodeError:
                            print("Could not decode chunk into JSON")
            yield {'type': 'urls', 'data': all_urls}

        except requests.exceptions.RequestException as e:
            print(f"Stream error: {e}")
            raise e
    
    

