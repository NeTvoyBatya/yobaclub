from pathlib import Path
import os
from json import load

BASE_DIR = Path(__file__).resolve().parent.parent


if os.getenv("HEROKU") is not None:
    DEBUG = False

    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

    CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        },
    }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv("DB_NAME"),
            'USER' : os.getenv("DB_USERNAME"),
            'PASSWORD' : os.getenv("DB_PASSWORD"),
            'HOST' : os.getenv("DB_HOST"),
            'PORT' : os.getenv("DB_PORT"),
        }
    }
else:
    with open("secrets.json", 'r', encoding="utf-8") as f:
        secrets = load(f)
    SECRET_KEY = secrets.get("django_secret_key")

    DEBUG = False

    CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'static', 'db.sqlite3')
    }
    }

ALLOWED_HOSTS = ['*']
#Maybe needed for loading youtube iframes
#SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yobaclub',
    'channels'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yobaclub.urls'

TEMPLATES = [
    {
        'NAME': 'jinja2',
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'static', 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            "environment": "yobaclub.settings.jinja2.environment"
        },
    },
]

#WSGI_APPLICATION = 'yobaclub.settings.wsgi.application'
ASGI_APPLICATION = 'yobaclub.settings.asgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases




AUTH_USER_MODEL = 'yobaclub.User'
AUTHENTICATION_BACKENDS = ['yobaclub.logic.auth.YobaBackend',]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
