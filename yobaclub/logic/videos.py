from dataclasses import dataclass
from httpx import AsyncClient
import asyncio
from requests import get
from os import getenv
from random import shuffle


imageext = ['png', 'jpg', 'jpeg']

def getAllThreadNums(board_name: str):
    res = get(f"https://2ch.hk/{board_name}/catalog.json").json()['threads']
    return [thread['num'] for thread in res]

def is_video_alright(fullname: str, used_names: dict):
    videoext = ['mp4', 'webm']
    this_is_video = fullname is not None and fullname.split('.')[-1].strip() in videoext
    video_is_unique = (used_names.get(fullname) is None or fullname.split('.')[-2] == 'videoplayback')
    return this_is_video and video_is_unique

async def getAllBoardMedia(board_name: str):
    data = { 'threads': {}, 'videos': []}
    threads_nums = getAllThreadNums(board_name)
    used_names = {}
    async with AsyncClient() as client:
        tasks = (client.get(f"https://2ch.hk/{board_name}/res/{thread_num}.json") for thread_num in threads_nums)
        reqs = await asyncio.gather(*tasks)
    for thread in reqs:
        thread = thread.json()
        posts = thread.get('threads')[0].get('posts')
        thread_num = posts[0].get('num')
        thread_url = f"https://2ch.hk/{board_name}/res/{thread_num}.html"
        thread_subject = posts[0].get('subjects')
        for post in posts:
            post_videos = [{'link': f"https://2ch.hk{post_file.get('path')}", 
                            'name': post_file.get("fullname"),
                            'post_num': post.get('num'), 
                            'thread_num': thread_num} 
                            for post_file in post.get('files')
                            if is_video_alright(post_file.get("fullname"), used_names)
                        ]
            
            for video in post_videos:
                used_names[video['name']] = True
            data.get('videos').extend(post_videos)
        data.get('threads').setdefault(thread_num, {'url': thread_url, 'subject': thread_subject})
    return data

def getVideos():
    if getenv("HEROKU") is None:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    res = asyncio.run(getAllBoardMedia('b'))
    shuffle(res["videos"])
    return res
     
