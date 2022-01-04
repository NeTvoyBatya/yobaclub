from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from yobaclub.logic.videos import getVideos
from yobaclub.logic.about import get_commits

@require_http_methods(["GET"])
def api_get_videos(request):
    return JsonResponse(
        getVideos(), 
        json_dumps_params={'ensure_ascii': False}, 
        content_type='application/json; charset=utf8'
    )

@require_http_methods(["GET"])
def api_get_commits(request):
    return JsonResponse(
        get_commits(),
        json_dumps_params={'ensure_ascii': False}, 
        content_type='application/json; charset=utf8',
        safe=False
    )