import requests
import json
import time
from progress.bar import IncrementalBar

with open ('settings.txt', 'r') as f:
    token = f.readline().strip()
    token_2 = f.readline().strip()

class VKdownloader():
    def __init__(self, token):
        self.token = token

    def download(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': '8928989',
            'album_id': 'profile',
            'access_token': self.token,
            'extended': '1',
            'photo_sizes': '1',
            'v': '5.131'
        }
        res = requests.get(url, params=params)
        return res.json()

    def get_data_for_json(self):
        photo_dict = {}
        content = self.download()
        max_size = 0
        for photo in content['response']['items']:
            for size in photo['sizes']:
                    if size['height'] >= max_size:
                        max_size = size['height']
            if photo['likes']['count'] not in photo_dict:
                photo_dict[photo['likes']['count']] = max_size
            else:
                photo_dict[f"{photo['likes']['count']}_{photo['id']}"] = max_size

        return photo_dict


    def get_all_photo(self):
        content = self.download()
        photo_dict = {}
        target_iterrations = content['response']['count']
        bar = IncrementalBar('Загрузка', max = target_iterrations)
        for photo in content['response']['items']:
            bar.next()
            max_size = 0
            for size in photo['sizes']:
                if size['height'] >= max_size:
                    max_size = size['height']
            if photo['likes']['count'] not in photo_dict:
                photo_dict[photo['likes']['count']] = max_size
            else:
                photo_dict[f"{photo['likes']['count']}_{photo['id']}"] = max_size
            for size in photo['sizes']:
                for names,sizes in photo_dict.items():
                    if sizes == size['height']:
                        photo_dict[names] = size['url']
                
                    
            time.sleep(0.33)
        bar.finish()
        return photo_dict

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
        response = requests.put(request_url, params=params,headers=self.get_headers())


    def upload(self, url, yandex_path):
        uri = 'v1/disk/resources/upload'
        request_url = self.base_host + uri
        params = {
            'url': url,
            'path': yandex_path
        }
        response = requests.post(request_url, params=params, headers=self.get_headers())
        



if __name__ == '__main__':
    vk = input('Вставьте ваш Токен VK: ')
    yd = input('Вставьте ваш Токен Яндекс Диска: ')
    download = VKdownloader(vk)
    uploader = YaUploader(yd)
    uploader.create_folder()
    for photo_name,photo_path in download.get_all_photo().items():
        uploader.upload(photo_path, f"VK/{photo_name}.jpg")
    for names,sizes in download.get_data_for_json().items():
        with open ('logs.json', 'a') as file:
            content = [{'file_name': f"{names}.jpg"},
            {'size': sizes}]
            a = json.dumps(content, indent=4, ensure_ascii=False)
            file.write(a)
    print('Загрзка на ваш Яндекс диск прошла успешно!')
            
