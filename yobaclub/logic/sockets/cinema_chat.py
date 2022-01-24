from channels.generic.websocket import AsyncJsonWebsocketConsumer
from urllib.parse import urlparse
from yobaclub.logic.cinema import ChatMessage, RoomUser, CinemaVideo
from yobaclub.models import CinemaRoom
from json import loads
from asgiref.sync import sync_to_async
from asyncio import sleep
from datetime import datetime

def get_youtube_links(message: str, links_indexes: list):
    links = []
    for indexes in links_indexes:
        link = message[indexes[0]:indexes[1]]
        parsed_link = urlparse(link)
        if parsed_link.netloc == "www.youtube.com" or parsed_link.netloc == "youtu.be" or parsed_link == "youtube.com":
            if not link in links:
                links.append(link)
    return links

def get_raw_links(message: str, links_indexes: list):
    links = []
    for indexes in links_indexes:
        link = message[indexes[0]:indexes[1]]
        parsed_link = urlparse(link)
        if parsed_link.path.endswith(".mp4") or parsed_link.path.endswith(".wemb"):
            if not link in links:
                links.append(link)
    return links
    

def find_links(message: str) -> list:
    words = message.split(" ")
    links = []
    for i, word in enumerate(words):
        for link_element in ["https://", "http://", "www.", ".com",]:
            if link_element in word:
                link_start = message.find(word, sum([len(w) for w in words[:i]]))
                links.append([link_start, link_start+len(word)])
                break
    return links

def get_room(room_id):
    try:
        room = CinemaRoom.objects.get(pk=room_id)
        return room
    except CinemaRoom.DoesNotExist:
        return None

class CinemaChatSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        room = await sync_to_async(get_room, thread_sensitive=True)(self.scope.get('url_route').get('kwargs').get('room_id'))
        if room is None:
            self.close()
            return
        self.room_name = room.room_id
        self.username = self.scope.get('user').name if not self.scope.get('user').is_anonymous else "Аноним"
        await self.channel_layer.group_add(f"chat-{self.room_name}", self.channel_name)
        await super().accept()
        await self.send_json({"type": "msg",
                              "text": f"Добро пожаловать в комнату {room.name}, {self.username}",
                              "links": [],
                              "author": "SYSTEM:",
                              "time": datetime.utcnow().timestamp()
                            })
        await self.send_json({"type": "history", "messages": [msg for msg in loads(room.messages)]})
        
        await sync_to_async(room.new_user, thread_sensitive=True)(RoomUser(
            self.channel_name, 
            self.scope.get('user')))
        if len(loads(room.users_in)) == 1:
            await sync_to_async(room.new_admin, thread_sensitive=True)()
        elif len(loads(room.users_in)) > 1:
            await sync_to_async(room.await_user, thread_sensitive=True)(RoomUser(
            self.channel_name, 
            self.scope.get('user')))
            await self.send_json({"type": "connect", "stage": "waiting_user", "users": await sync_to_async(room.public_users, thread_sensitive=True)(), "title": room.name})
        return
    
    async def disconnect(self, code):
        room = await sync_to_async(get_room, thread_sensitive=True)(self.room_name)
        await sync_to_async(room.remove_user, thread_sensitive=True)(self.channel_name)
        if room.admin == self.channel_name:
            admin = await sync_to_async(room.new_admin, thread_sensitive=True)()
        await self.channel_layer.group_discard(f"chat-{self.room_name}", self.channel_name)
        leave_message = ChatMessage(f"{self.username} Выходит из комнаты", [], "SYSTEM")
        await self.broadcast_message(leave_message)
        return await super().disconnect(code)
    
    async def broadcast_message(self, message: ChatMessage):
        await self.channel_layer.group_send(f"chat-{self.room_name}",
                {
                    "type": "chat.broadcast",
                    "content":
                        {
                            "type": "msg",
                            "text": message.text,
                            "links": message.links,
                            "author": message.author+":",
                            "time": message.time
                        }
                }
            )
    
    async def broadcast_video(self, video: CinemaVideo):
        await self.channel_layer.group_send(f"chat-{self.room_name}",
            {
                "type": "chat.broadcast",
                "content":
                    {
                        "type": "new_video",
                        "provider": video.provider,
                        "link": video.link,
                        "author": video.author
                    }
            }
        )

    async def broadcast_state(self, state_content : dict, sender: str):
        await self.channel_layer.group_send(f"chat-{self.room_name}",
            {
                "sender": sender,
                "type": "broadcast.except.sender",
                "content": state_content
            }
        )
    
    async def send_to_users(self, state_content: dict, send_to :list):
        await self.channel_layer.group_send(f"chat-{self.room_name}",
            {
                "send_to": send_to,
                "type": "broadcast.to.users",
                "content": state_content
            }
        )

     
    async def receive_json(self, content, **kwargs):
        if content.get("type") == "msg":
            text = content["text"]
            message_link_parts = find_links(text)
            author = self.scope["user"].name if self.scope["user"].is_anonymous == False else "Аноним"

            if len(message_link_parts) > 0:
                youtube_links = get_youtube_links(text, message_link_parts)
                raw_links = get_raw_links(text, message_link_parts)
                for link in youtube_links:
                    video = CinemaVideo(link, "youtube", author)
                    await self.broadcast_video(video)
                for link in raw_links:
                    video = CinemaVideo(link, "raw", author)
                    await self.broadcast_video(video)
            message = ChatMessage(text, message_link_parts, author)
            room = await sync_to_async(get_room, thread_sensitive=True)(self.room_name)
            await sync_to_async(room.add_message, thread_sensitive=True)(message)
            await self.broadcast_message(message)
            return
        if content.get("type") == "state_changed":
            state = content.get("state")
            if state == "paused" or state == "playing":
                await self.broadcast_state({"type": "state_changed", "state": state}, self.channel_name)
                return
            if state == "seeking":
                await self.broadcast_state({"type": "state_changed", "state": state, "seek_to": content.get("seek_to")}, self.channel_name)
                return
        if content.get("type") == "connect":
            if content.get("stage") == "user_ready":
                await self.broadcast_state({"type": "msg",
                                            "text": f"{self.username} Присоединяется к комнате.",
                                            "links": [],
                                            "author": "SYSTEM:",
                                            "time": datetime.utcnow().timestamp()
                                          }, self.channel_name)
                room = await sync_to_async(get_room, thread_sensitive=True)(self.room_name)
                admin = room.admin
                await self.broadcast_state({"type": "state_changed", "state": "paused"}, 'nobody')
                await sleep(1)
                await self.send_to_users({"type": "state_asked"}, [admin,])
        if content.get("type") == "asked_state":
            print(content)
            room = await sync_to_async(get_room, thread_sensitive=True)(self.room_name)
            users = [user.get("channel_name") for user in loads(room.waiting_users)]
            if content.get("error") == None:
                await self.send_to_users({"type": "connect",
                                          "stage": "done", 
                                          "link": content.get('link'),
                                          "provider": content.get("provider"),
                                          "author": content.get("author"),
                                          "time": content.get("time")}, users)
            else:
                await self.send_to_users({"type": "connect",
                                          "stage": "done", 
                                          "error": "novideo"}, users)
            
    async def chat_broadcast(self, event):
        await self.send_json(
                event.get("content")
            )
    
    async def broadcast_except_sender(self, event):
        if self.channel_name != event.get("sender"):
            await self.send_json(
                event.get("content")
            )
    async def broadcast_to_users(self, event):
        if self.channel_name in event.get("send_to"):
            await self.send_json(
                event.get("content")
            )
