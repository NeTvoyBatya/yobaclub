from django.template import loader
from django.http import HttpResponse

def cookie_to_classname(str: str):
    return ''.join([string.capitalize() for string in str.split('_')])

def render(request, template_name, context=None, content_type=None, status=None, using=None):
    """
    Return a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    if context is None:
        context = {}
    if request.COOKIES.get('lkklchesdf') is not None:
        context['secret_theme'] = True
    else:
        context['secret_theme'] = False
    if request.COOKIES.get('theme') is not None:
        context['theme'] = cookie_to_classname(request.COOKIES.get('theme'))
        if request.COOKIES.get('theme') == 'secret' and request.COOKIES.get('lkklchesdf') is None:
            context['theme'] = cookie_to_classname('samurai')
            request.COOKIES.setdefault('theme', 'samurai')
    content = loader.render_to_string(template_name, context, request, using=using)
    return HttpResponse(content, content_type, status)