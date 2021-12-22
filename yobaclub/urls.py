from django.contrib import admin
from yobaclub import views, api_views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('cinema', views.cinema, name='cinema'),
    path('gallery', views.gallery, name='gallery'),
    path('sign-in', views.sign_in, name = 'sign_in'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('test', views.test, name='test'),

    path('api/get_videos', api_views.api_get_videos, name = 'api_get_videos')
]
