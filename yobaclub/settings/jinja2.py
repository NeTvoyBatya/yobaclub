from jinja2 import Environment
from django.urls import reverse
from django.contrib.staticfiles.storage import staticfiles_storage
# from django.templatetags.static import static

def jinja_url(viewname, *args, **kwargs):
    return reverse(viewname, args=args, kwargs=kwargs)

def environment(**options):
	env = Environment(**options)
	env.globals.update({
		"static": staticfiles_storage.url,
		"url": jinja_url
	})
	return env