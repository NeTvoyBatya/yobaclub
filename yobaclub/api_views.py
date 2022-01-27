from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from yobaclub.logic.videos import getVideos
from yobaclub.logic.about import get_commits
from yobaclub.logic.gallery import get_things
from yobaclub.logic.cinema import get_rooms
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt
from yobaclub.logic.utils.vk_loader import VKLoader
from json import load, loads
from urllib.request import urlretrieve
from os import path, remove


VIDEO_DESCRIPTION = '''Видео от USERNAME.
YOBACLUB: http://yobatube.herokuapp.com
DISCORD: https://discord.com/invite/PVpMB5Yuew
VK: https://vk.com/zolupaofficial'''
#TODO: MOVE THIS SHIT SOMEWHERE ELSE

@require_http_methods(["GET"])
def api_get_videos(request: WSGIRequest):
    return JsonResponse(
        getVideos(), 
        json_dumps_params={'ensure_ascii': False}, 
        content_type='application/json; charset=utf8'
    )

@require_http_methods(["GET"])
def api_get_commits(request: WSGIRequest):
    return JsonResponse(
        get_commits(),
        json_dumps_params={'ensure_ascii': False}, 
        content_type='application/json; charset=utf8',
        safe=False
    )

@require_http_methods(["GET"])
def api_get_things(request: WSGIRequest):
    return JsonResponse(
        get_things(),
        json_dumps_params={'ensure_ascii': False}, 
        content_type='application/json; charset=utf8',
        safe=False
    )

@require_http_methods(["GET"])
def api_get_cinema_rooms(request: WSGIRequest):
    return JsonResponse(
        get_rooms(),
        json_dumps_params={'ensure_ascii': False}, 
        content_type='application/json; charset=utf8',
        safe=False
    )

@csrf_exempt
@require_http_methods(["POST"])
def api_post_video(request: WSGIRequest):
    if request.user.is_anonymous:
        return JsonResponse(
            {"result": "fail", "text": "Вы должны быть авторизованы для постинга видео"},
            json_dumps_params={'ensure_ascii': False}, 
            content_type='application/json; charset=utf8',
            safe=False)
    if not request.user.can_post:
        return JsonResponse(
            {"result": "fail", "text": "У вас нет прав для постинга видео"},
            json_dumps_params={'ensure_ascii': False}, 
            content_type='application/json; charset=utf8',
            safe=False)

    data = loads(request.body.decode())
    with open('secrets.json', 'r', encoding='utf-8') as f:
            vk_token = load(f).get('vk_upload_video_token')
    loader = VKLoader(vk_token)
    file_saved = False
    video_file = None

    try:
        file_path = path.join('yobaclub', 'static', 'uploads', data.get('src').split('/')[-1])
        video_file = open( urlretrieve( data.get('src'), file_path )[0], 'rb' )
        file_saved = True
    except:
        if file_saved and path.isfile(file_path):
            if not video_file.closed:
                video_file.close()
            remove(file_path)
        return JsonResponse(
        {"result": "fail", "text": "К сожалению, мы не можем получить это видео"},
            json_dumps_params={'ensure_ascii': False}, 
            content_type='application/json; charset=utf8',
            safe=False)
    
    try:
        video_name = str(loader.get_videos(-163806918).get('response').get('count')+1)
        video_id = loader.upload_video(
            video_file,
            video_name,
            VIDEO_DESCRIPTION.replace("USERNAME", request.user.name),
            163806918
            ).get('url')
        attachment = f"video{video_id}"
        if data.get("title") is not None and len(data.get("title"))> 0:
            loader.wall_post(-163806918, from_group=1, attachments=attachment, message=data.get('title'))
        else:
            loader.wall_post(-163806918, from_group=1, attachments=attachment)
        if file_saved and path.isfile(file_path):
            if not video_file.closed:
                video_file.close()
            remove(file_path)
        return JsonResponse(
            {"result": "success", "text": "Пост скоро появится в группе"},
            json_dumps_params={'ensure_ascii': False}, 
            content_type='application/json; charset=utf8',
            safe=False)
    except:
        if file_saved and path.isfile(file_path):
            if not video_file.closed:
                video_file.close()
            remove(file_path)
        return JsonResponse(
            {"result": "fail", "text": "Ошибка при загрузке видео в группу"},
            json_dumps_params={'ensure_ascii': False}, 
            content_type='application/json; charset=utf8',
            safe=False)
