import requests
from progress.bar import IncrementalBar
import time

class VkDownloader():
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
        res = requests.get(url, params = params)
        return res.json()


    def get_data_for_json(self):
        photo_dict = {}
        content = self.download()
        max_size = 0
        for photo in content['response']['items']:
            likes = photo['likes']['count'] 
            for size in photo['sizes']:
                    if size['height'] >= max_size:
                        max_size = size['height']
            if likes not in photo_dict:
                photo_dict[likes] = max_size
            else:
                photo_dict[f"{likes}_{photo['id']}"] = max_size

        return photo_dict


    def get_all_photo(self):
        content = self.download()
        photo_dict = {}
        target_iterrations = content['response']['count']
        bar = IncrementalBar('Загрузка', max = target_iterrations)
        for photo in content['response']['items']:
            bar.next()
            max_size = 0
            likes = photo['likes']['count'] 
            for size in photo['sizes']:
                if size['height'] >= max_size:
                    max_size = size['height']
            if likes not in photo_dict:
                photo_dict[likes] = max_size
            else:
                photo_dict[f"{likes}_{photo['id']}"] = max_size
            for size in photo['sizes']:
                for names,sizes in photo_dict.items():
                    if sizes == size['height']:
                        photo_dict[names] = size['url']    
            time.sleep(0.33)
        bar.finish()
        return photo_dict