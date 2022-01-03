from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.handlers.wsgi import WSGIRequest
from yobaclub.logic.utils import forms
from yobaclub.logic.utils import models
from yobaclub.logic.utils.themedRender import render

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

@require_http_methods(["GET", "POST"])
def sign_in(request: WSGIRequest):
    return HttpResponse(render(request, 'SignIn.html'))

@csrf_exempt
@require_http_methods(["GET", "POST"])
def sign_up(request: WSGIRequest):
    if request.method.lower() == 'get':
        return HttpResponse(render(request, 'SignUp.html'))
    form = forms.SignUpForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        new_user = models.User(name=form_data['login'],
                               password = form_data['password'],
                               mail = form_data['mail'])
        new_user.save()
        return redirect('index')
    else:
        return HttpResponse(render(request, '<h1>503 ERROR</h1>', status=503)) #TODO: ERROR PAGE TEMPLATE
    

@require_http_methods(["GET"])
def test(request: WSGIRequest):
    return HttpResponse(render(request, 'base.html'))
