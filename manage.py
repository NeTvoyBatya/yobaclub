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


#----MULTINOTE------
#TODO: CUSTOM FILES UPLOADING INTERFACE AT GALLERY
#TODO: JOKES IN THEMED RENDER AS CONTEXT VARIABLE TO LOADING SCREEN