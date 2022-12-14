import json
import configparser 
import Vkmodul
import Ydmodul

config = configparser.ConfigParser() 
config.read("settings.ini")
vktoken = config["Tokens"]["vk"]
ydtoken = config["Tokens"]["yd"]


def jsonlogs():
    for names,sizes in download.get_data_for_json().items():
        with open ('logs.json', 'a') as file:
            content = [
                {'file_name': f"{names}.jpg"},
                {'size': sizes}]
            a = json.dumps(
                content, 
                indent = 4, 
                ensure_ascii = False
                )
            file.write(a)


if __name__ == '__main__':
    download = Vkmodul.VkDownloader(vktoken)
    uploader = Ydmodul.YaUploader(ydtoken)
    uploader.create_folder()
    for photo_name,photo_path in download.get_all_photo().items():
        uploader.upload(photo_path, f"VK/{photo_name}.jpg")
    jsonlogs()    
    print('Загрузка на ваш Яндекс диск прошла успешно!')
