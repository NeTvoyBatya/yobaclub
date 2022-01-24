from datetime import datetime
from yobaclub.models import CinemaRoom
from json import loads, dumps


class ChatMessage:
    def __init__(self, text, links, author) -> None:
        self.text = text
        self.links = links
        self.author = author
        self.time = datetime.utcnow().timestamp()

    def __dict__(self):
            return {"text": self.text, "links": self.links, "author": self.author+":", "time": self.time}

class CinemaVideo:
    def __init__(self, link, provider, author) -> None:
        self.link = link
        self.provider = provider
        self.author = author
    
    def __dict__(self):
        return {"provider": self.provider, "link": self.link, "author": self.author}

class RoomUser:
    def __init__(self, channel_name: str, user) -> None:
        self.channel_name = channel_name
        self.logged_in = True if not user.is_anonymous else False
        self.name = user.name if not user.is_anonymous else "Аноним"
    
    def __dict__(self):
        return {"name": self.name, "channel_name": self.channel_name, "logged_in": self.logged_in}

    def __public_dict__(self):
        return {"name": self.name, "logged_in": self.logged_in}

def get_rooms():
    rooms = [
        {
            "room_id": room.room_id,
            "room_name": room.name,
            "login_only": room.login_only,
            "users_in": [user for user in loads(room.users_in)]
            
        } for room in CinemaRoom.objects.all()
    ]
    for room in rooms:
        for user in room["users_in"]:
            user.pop('channel_name', None)
    rooms.reverse()
    return rooms