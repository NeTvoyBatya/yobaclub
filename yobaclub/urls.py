from django.contrib import admin
from yobaclub import views, api_views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('cinema', views.cinema, name='cinema'),
    path('about', views.about, name='about'),
    path('video', views.video, name='video'),
    path('gallery', views.gallery, name='gallery'),
    path('sign-in', views.sign_in, name = 'sign_in'),
    path('sign-up', views.sign_up, name='sign_up'),
    path('logout', views.logout, name='logout'),

    path('api/get_videos', api_views.api_get_videos, name = 'api_get_videos'),
    path('api/get_commits', api_views.api_get_commits, name = 'api_get_commits')
]
