import requests
import json


class ClientFasttext:
    def __init__(self, url, token):
        self.url = url[:-1] if url[-1] == '/' else url
        self._TOKEN = token
        self.size_vector = 60

    def get_most_similar(self, word: str, topn: int = 30):
        result = requests.post(
            url=f'{self.url}/get_most_similar', data={"token": self._TOKEN, "data": word, "topn": topn})
        if result.status_code == 200:
            result = result.json()
        else:
            return None
        if result['status'] == 'ok':
            return result['result']
        return None

    def get_vector(self, line, is_tokenize=True):
        return requests.post(headers={'Content-Type': 'application/json'},
                             url=f'{self.url}/get_vector',
                             data=json.dumps({"token": self._TOKEN, "data": line,
                                              "is_tokenize": is_tokenize})).json()['result']
