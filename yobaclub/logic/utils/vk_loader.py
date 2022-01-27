import requests
from json import dump

class VKLoader():
    def __init__(self, token: str) -> None:
        self.token = token
        self.api_link = "https://api.vk.com/method/"
        self.api_version = 5.131
    
    def get_api_link(self, method_name: str, params_dict: dict):
        params_dict.setdefault('access_token', self.token)
        params_dict.setdefault('v', self.api_version)
        params = ""
        for key in params_dict.keys():
            param_key = key
            param_value = params_dict.get(key)
            if param_value is None:
                continue
            if type(param_value) == bool:
                if param_value:
                    param_value = 1
                else:
                    param_value = 0
            params+=f"{param_key}={param_value}&"
        return f"{self.api_link}{method_name}?{params}"[:-1]

    def upload_photos(self, group_id: int, album_id: int, photo):
        ask_response = requests.get(
            self.get_api_link(
                "photos.getUploadServer",
                {
                    'album_id': album_id,
                    'group_id': group_id
                }))
        if not ask_response.ok:
            return None
        ask_response = ask_response.json()
        files={"file1": photo}
        upload_response = requests.post(ask_response.get('response').get('upload_url'), files=files)
        if not upload_response.ok:
            return None
        upload_response = upload_response.json()
        saving_response = requests.get(
            self.get_api_link(
                "photos.save",
                {
                    'album_id': album_id,
                    'group_id': group_id,
                    'server': upload_response.get('server'),
                    'photos_list': upload_response.get('photos_list'),
                    'hash': upload_response.get('hash')
                }))
        if not saving_response.ok:
            return None
        saving_response = saving_response.json()
        uploaded_images = saving_response.get('response')
        uploaded_images[0].get('sizes').sort(key=lambda image: (image.get('height')+image.get('width'))/2 )
        return {"type": "image", "url": uploaded_images[0].get('sizes')[-1].get('url')}
    
    def upload_video(self, video_obj, video_name: str, video_description: str, group_id: int,
                     no_comments:bool=False, repeat:bool=False, album_id: int=None):
        ask_response = requests.get(
            self.get_api_link('video.save',
                {
                    "name": video_name,
                    "description": video_description,
                    "group_id": group_id,
                    "album_id": album_id,
                    "no_comments": no_comments,
                    "repeat": repeat
                }))
        if not ask_response.ok:
            return
        ask_response = ask_response.json()
        upload_response = requests.post(ask_response.get('response').get('upload_url'),
                          files={'video_file': video_obj})
        if not upload_response.ok:
            return
        upload_response = upload_response.json()
        return {"type": "video", "url": f"{upload_response.get('owner_id')}_{upload_response.get('video_id')}"}

    def upload_file(self, file_obj, group_id: int, file_title: str):
        ask_response = requests.get(
            self.get_api_link(
                'docs.getUploadServer',
                {"group_id": group_id}))
        if not ask_response.ok:
            return
        ask_response = ask_response.json()
        upload_response = requests.post(ask_response.get('response').get('upload_url'), files={'file': file_obj})
        if not upload_response.ok:
            return
        upload_response = upload_response.json()
        save_response = requests.get(
            self.get_api_link(
                'docs.save',
                {
                    'file': upload_response.get('file'),
                    'title': file_title
                }))
        if not save_response.ok:
            return
        save_response = save_response.json()
        save_response = save_response.get('response')
        saved_file_link = save_response.get(save_response.get('type')).get('url')
        return {'type': 'doc', 'name': file_title, 'url': saved_file_link}
    
    def get_videos(self, owner_id: int, album_id: int=None, count: int=1, offset: int=0):
        params = {
            "owner_id": owner_id,
            "count": count,
            "offset": offset
        }
        if album_id is not None:
            params["album_id"] = album_id
        response = requests.get(self.get_api_link("video.get", params))
        return response.json()
    
    def wall_post(self, owner_id: int, from_group: int=0, message: str=None, attachments: str=None):
        params = {
            "owner_id": owner_id,
            "from_group": from_group,
        }
        if attachments is not None:
            params["attachments"] = attachments
        if message is not None:
            params["message"] = message
        response = requests.get(self.get_api_link("wall.post", params))
        return response.json()