from pathlib import Path
import os
from json import load


BASE_DIR = Path(__file__).resolve().parent.parent


if os.getenv("HEROKU") is not None:
    DEBUG = False

    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

    #Thanks, Heroku for not allowing Russians to use Redis
    #CHANNEL_LAYERS = {
    #    'default': {
    #        'BACKEND': 'channels_redis.core.RedisChannelLayer',
    #        'CONFIG': {
    #            "hosts": ["redis://:redishost"],
    #        },
    #    },
    #}
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
            },
    }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv("DATABASE_URL").split("/")[-1],
            'USER' : os.getenv("DATABASE_URL").split(":")[1][2:],
            'PASSWORD' : os.getenv("DATABASE_URL").split("@")[0].split(":")[2],
            'HOST' : os.getenv("DATABASE_URL").split("@")[1].split(":")[0],
            'PORT' : os.getenv("DATABASE_URL").split("@")[1].split(":")[1].split("/")[0],
        }
    }
else:
    with open("secrets.json", 'r', encoding="utf-8") as f:
        secrets = load(f)
    SECRET_KEY = secrets.get("django_secret_key")

    DEBUG = True

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
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

WSGI_APPLICATION = 'yobaclub.settings.wsgi.application'
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
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
