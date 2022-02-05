from django.contrib import admin
from yobaclub import views, api_views
from django.urls import path
from yobaclub.models import CinemaRoom

rooms = CinemaRoom.objects.all()
for room in rooms:
    room.delete()

urlpatterns = [
    path('', views.index, name='index'),
    path('cinema', views.cinema, name='cinema'),
    path('cinema/<str:room_id>/', views.cinema_room, name='cinema_room'),
    path('about', views.about, name='about'),
    path('video', views.video, name='video'),
    path('gallery', views.gallery, name='gallery'),
    path('sign-in', views.sign_in, name = 'sign_in'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('logout', views.logout, name='logout'),

    path('api/get_videos', api_views.api_get_videos, name = 'api_get_videos'),
    path('api/get_commits', api_views.api_get_commits, name = 'api_get_commits'),
    path('api/get_things', api_views.api_get_things, name='apo_get_things'),
    path('api/get_cinema_rooms', api_views.api_get_cinema_rooms, name='api_get_cinema_rooms'),
    path('api/post_video', api_views.api_post_video, name='api_post_video'),
    path('api/get_track', api_views.api_get_music, name='api_get_track')
]
