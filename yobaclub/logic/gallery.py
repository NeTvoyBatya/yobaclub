from yobaclub.models import Thing

def get_things():
    things = [
        {
            "name": thing.title,
            "description": thing.description,
            "files": thing.files_links,
            "author": thing.author
        } for thing in Thing.objects.all()]
    return things