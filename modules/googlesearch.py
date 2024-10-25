import requests

class GoogleSearch:

    def __init__(self, api_key, engine_id):
        """
            Init Google Search.
            Args:
                api_key (str): Api Key Google
                engine_id (str): Engine Id Google
        """
        self.api_key = api_key
        self.engine_id = engine_id
    
    def search(self, query, start_page=1, pages=1, lang="lang_es"):
        """Make a request google api"""
        final_result = []
        results_per_page = 10
        for page in range(pages):
            start_index = (start_page - 1) * results_per_page + 1 + (page * results_per_page)
            url = f"https://www.googleapis.com/customsearch/v1?key={self.api_key}&cx={self.engine_id}&q={query}&start={start_index}&lr={lang}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                if not data.get('items'):
                    print('No results found in page: ', page+1)
                    break
                results = self.custom_results(data.get('items'))
                final_result.extend(results)
            else:
                print('Erro al consultar datos')
                break
        return final_result
    
    def custom_results(self, results):
        """Filter results."""
        custom_results = []
        for r in results:
            result = {
                "title": r.get('title'),
                "description": r.get('snippet'),
                "link": r.get('link')
            }
            custom_results.append(result)
        return custom_results
 