#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yobaclub.settings.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if len(sys.argv) <2:
        sys.argv.append("runserver")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

#TODO: ERROR PAGES TEMPLATES
#TODO: ADD VIDEO POSTING TO VIDEOS, MAYBE WITH VK AUTH
#TODO: MUSIC RECOGNITION AT VIDEOS
#TODO: MOVE SECRET TOKEN IN SETTINGS TO ENV AND CHANGE IT
#TODO: AUTO SET DEBUG TO FALSE IF FOUND HEREKUENV VARIABLE
#TODO: DEPLOY REDIS SERVER ON HEROKU
#TODO: AUTO SET SOCKETS BACKEND TO REDIS ON HEROKU DUE TO SAFETY NEEDS
#TODO: CHAT MESSAGES ON STATE CHANGING AT CINEMA
#TODO: ADD STATE TO HISTORY AT CINEMA
#TODO: VIDEOS QUEUE AT CINEMA
#TODO: PUBLIC ROOMS AND LOGIN-ONLY ROOMS AT CINEMA
#TODO: CLOSE MENU ON CLICK OUT OF IT BOUNDARIES AT INDEX
#TODO: CUSTOM FILES UPLOADING INTERACE AT GALLERY
#TODO: SHOW AUTHOR AT GALLERY
#TODO: SHOW ADDITIONAL FILES AT GALLERY
#TODO: JOKES IN THEMED RENDER AS CONTEXT VARIABLE TO LOADING SCREEN
#BUG: SAVED THEME DISAPPEARS AFTER PC REBOOTING, MAYBE BECAUSE OF 0 SET IN COOKIES EXPIRES_TIME