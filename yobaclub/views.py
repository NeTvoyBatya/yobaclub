from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest
from yobaclub import forms
from yobaclub.logic.utils.themedRender import render
from yobaclub.logic.utils.redirect_back import redirect_back_or_index
from django.contrib.auth import logout as logout_user

@require_http_methods(["GET"])
def index(request: WSGIRequest):
    return HttpResponse(render(request, 'Index.html'))

@require_http_methods(["GET"])
def cinema(request: WSGIRequest):
    return HttpResponse(render(request, 'Cinema.html'))

@require_http_methods(["GET"])
def about(request: WSGIRequest):
    return HttpResponse(render(request, 'About.html'))

@require_http_methods(["GET"])
def gallery(request: WSGIRequest):
    return HttpResponse(render(request, 'gallery.html'))

@require_http_methods(["GET"])
def video(request: WSGIRequest):
    return HttpResponse(render(request, 'video.html'))

@csrf_exempt
@require_http_methods(["GET", "POST"])
def sign_in(request: WSGIRequest):
    if request.method.lower() == 'get':
        return HttpResponse(render(request, 'SignIn.html'))
    form = forms.SignInForm(request.POST)
    if form.is_valid():
        if form.login_user(request):
            return redirect('index')
    return HttpResponse(render(request, 'SignIn.html')) 

@csrf_exempt
@require_http_methods(["GET", "POST"])
def sign_up(request: WSGIRequest):
    if request.method.lower() == 'get':
        return HttpResponse(render(request, 'SignUp.html'))
    form = forms.SignUpForm(request.POST)
    if form.is_valid():
        if form.save_user():
            return redirect('sign_in')
    return HttpResponse(render(request, '<h1>503 ERROR</h1>', status=503)) 
    
@require_http_methods(["GET"])
def logout(request: WSGIRequest):
    if not request.user.is_anonymous:
        logout_user(request)
    return redirect_back_or_index(request)
    
