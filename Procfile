release: python manage.py migrate --no-input
web: daphne -b 0.0.0.0 -p $PORT yobaclub.settings.asgi:application -v2