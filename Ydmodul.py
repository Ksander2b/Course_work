import requests

class YaUploader():
    def __init__(self, token):
        self.base_host = 'https://cloud-api.yandex.net:443/'
        self.token = token


    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
            }


    def create_folder(self):
        uri = 'v1/disk/resources'
        request_url = self.base_host + uri
        params = {
            'path': 'VK',
            }
        response = requests.put(
            request_url, 
            params = params,
            headers = self.get_headers()
            )


    def upload(self, url, yandex_path):
        uri = 'v1/disk/resources/upload'
        request_url = self.base_host + uri
        params = {
            'url': url,
            'path': yandex_path
            }
        response = requests.post(
            request_url,
            params = params, 
            headers = self.get_headers()
            )
