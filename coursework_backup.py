import requests
from pprint import pprint
import os


with open('token.txt', 'r') as file_object:
    token = file_object.read().strip()

with open('ya_token_1.txt', 'r') as file_object:
    ya_token = file_object.read().strip()

class VkUser:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photo(self, owner_id):
        get_photo_url = self.url + 'photos.get'
        params = {
            'album_id': 'profile',
            'owner_id': owner_id,
            'rev': '0',
            'extended': '1',
            'feed_type': 'photo',
            'photo_sizes': '0',
            'access_token': token,
            'v': '5.131'
        }
        req = requests.get(get_photo_url, params={**self.params, **params}).json()
        photo_data = req['response']['items']
        for i in photo_data:
            dic = (i['sizes'][-1])
            photo_url = dic['url']
            photo_name = i['likes']['count']
            download_photo = requests.get(photo_url)
            with open(os.path.join('photos', f'{photo_name}.jpg'), 'wb') as file:
                file.write(download_photo.content)
            return 'Фотографии загружены!'


class YaUploader:
     def __init__(self, token: str):
         self.token = token

     def get_headers(self):
         return {
             'Content-Type': 'application/json',
             'Authorization': 'OAuth {}'.format(self.token)
         }

     def get_files_list(self):
         files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
         headers = self.get_headers()
         response = requests.get(files_url, headers=headers)
         return response.json()

     def _get_upload_link(self, disk_file_path):
         upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
         headers = self.get_headers()
         params = {"path": disk_file_path, "overwrite": "true"}
         response = requests.get(upload_url, headers=headers, params=params)
         pprint(response.json())
         return response.json()

     def upload_file_to_disk(self, disk_file_path, filename):
         href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
         response = requests.put(href, data=open(filename, 'rb'))
         response.raise_for_status()
         if response.status_code == 201:
             print("Success")


def create_folder(folder):
    if not os.path.isdir(folder): # проверяет наличие каталога/директрии
        os.mkdir(folder) # создает каталог с именем () с режимом доступа


def photos_from_folder(folder) -> list:
    file_list = os.listdir(folder) #возвращает список, содержащий имена файлов и директорий в каталоге
    return file_list


if __name__ == '__main__':
    create_folder('photos')
    vk_client = VkUser(token, '5.131')
    pprint(vk_client.get_photo('25078531'))
    file_list = photos_from_folder('photos')
    ya = YaUploader(token=ya_token)
    ya.upload_file_to_disk('photos', file_list)
