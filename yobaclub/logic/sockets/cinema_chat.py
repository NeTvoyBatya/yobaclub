from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from urllib.parse import urlparse
from datetime import datetime

MESSAGES = []

class ChatMessage:
    def __init__(self, text, links, author) -> None:
        self.text = text
        self.links = links
        self.author = author
        self.time = datetime.utcnow().timestamp()
    
    def __dict__(self):
        return {"text": self.text, "links": self.links, "author": self.author+":", "time": self.time}


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

class CinemaChatSocket(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("chat", self.channel_name)
        await super().accept()
        await self.send_json({"type": "history", "messages": [msg.__dict__() for msg in MESSAGES]})
        return
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard("chat", self.channel_name)
        return await super().disconnect(code)
    
    async def broadcast_message(self, message: ChatMessage):
        await self.channel_layer.group_send("chat",
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

    async def broadcast_new_video(self, links: list, author: str, video_provider):
            await self.channel_layer.group_send("chat",
                {
                    "type": "chat.broadcast",
                    "content":
                            {
                                "type": "new_video",
                                "videos": links,
                                "author": author,
                                "provider": video_provider
                            }
                }
            )
    
    async def broadcast_state(self, state_content: dict, sender):
        await self.channel_layer.group_send("chat",
            {
                "type": "chat.broadcast.state",
                "sender": sender,
                "content": {
                    "type": "video_state_changed",
                    "state_content": state_content
                }
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
                if len(youtube_links) > 0:
                    await self.broadcast_new_video(youtube_links, author, "youtube")
                if len(raw_links) > 0:
                    await self.broadcast_new_video(raw_links, author, "raw")
            message = ChatMessage(text, message_link_parts, author)
            MESSAGES.append(message)
            await self.broadcast_message(message)
            return
        if content.get("type") == "video_state_changed":
            if content.get("state") == "paused":
                await self.broadcast_state({"state_type": "paused"}, self.channel_name)
                return
            if content.get("state") == "playing":
                await self.broadcast_state({"state_type": "playing"}, self.channel_name)
                return
            if content.get("state") == "seeking":
                await self.broadcast_state({"state_type": "seeking", "seek_to": content.get("seek_to")}, self.channel_name)

    async def chat_broadcast(self, event):
        await self.send_json(
                event.get("content")
            )
    async def chat_broadcast_state(self, event):
        if self.channel_name != event.get("sender"):
            await self.send_json(
                event.get("content")
            )
