import requests
from progress.bar import IncrementalBar
import time

class VkDownloader():
    def __init__(self, token):
        self.token = token
        self.name = input('Введите id или screen_name пользователя: ')
        self.count = input('Сколько фотографий вы хотите скачать: ')


    def _get_id(self):
        url = 'https://api.vk.com/method/utils.resolveScreenName'
        params = {
            'screen_name': self.name,
            'access_token': self.token,
            'v': '5.131'
            }
        res = requests.get(url, params = params)
        result = res.json()['response']
        return result


    def download(self):
        url = 'https://api.vk.com/method/photos.get'
        id = self._get_id()
        if id == []:
            name = self.name
        else:
            name = id['object_id']
        params = {
            'owner_id': name,
            'album_id': 'profile',
            'access_token': self.token,
            'extended': '1',
            'photo_sizes': '1',
            'count': self.count,
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
        bar = IncrementalBar('Загрузка', max = int(self.count))
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