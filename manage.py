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
        sys.argv.append("--insecure")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

#----NIKITOS--------
#TODO: ERROR PAGES TEMPLATES
#TODO: SHOW AUTHOR AT GALLERY
#TODO: SHOW ADDITIONAL FILES AT GALLERY
#BUG: SCROLLBAR ON PAGE "ABOUT US" ARE SHOWN IN FIREFOX

#----MAMANYA--------
#BUG: FILES UPLOADING TO VK MULTIPLE TIMES AT GALLERY \\ #NOTE: CAN'T REPRODUCE, FIXED?

#TODO: MOVE SECRET TOKEN IN SETTINGS TO ENV AND CHANGE IT
#TODO: DEPLOY REDIS SERVER ON HEROKU
#TODO: AUTO SET SOCKETS BACKEND TO REDIS ON HEROKU DUE TO SAFETY NEEDS

#----MULTINOTE------
#TODO: CUSTOM FILES UPLOADING INTERFACE AT GALLERY
#TODO: JOKES IN THEMED RENDER AS CONTEXT VARIABLE TO LOADING SCREEN