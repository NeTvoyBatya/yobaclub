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
        print(link)
        parsed_link = urlparse(link)
        if parsed_link.netloc == "www.youtube.com" or parsed_link.netloc == "youtu.be" or parsed_link == "youtube.com":
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

    async def broadcast_new_video(self, links: list, author: str):
            await self.channel_layer.group_send("chat",
                {
                    "type": "chat.broadcast",
                    "content":
                            {
                                "type": "new_video",
                                "videos": links,
                                "author": author
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
                if len(youtube_links) > 0:
                    await self.broadcast_new_video(youtube_links, author)
            message = ChatMessage(text, message_link_parts, author)
            MESSAGES.append(message)
            await self.broadcast_message(message)

    async def chat_broadcast(self, event):
        await self.send_json(
                event["content"]
            )