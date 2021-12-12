from dataclasses import dataclass
import httpx
import asyncio
import requests
from os import environ


videoext = ['mp4', 'webm']
imageext = ['png', 'jpg', 'jpeg']

def getAllThreadNums(board_name: str):
    res = requests.get(f"https://2ch.hk/{board_name}/catalog.json").json()['threads']
    return [thread['num'] for thread in res]
    
async def getAllBoardMedia(board_name: str):
    data = { 'threads': {}, 'videos': []}
    threads_nums = getAllThreadNums(board_name)
    async with httpx.AsyncClient() as client:
        tasks = (client.get(f"https://2ch.hk/{board_name}/res/{thread_num}.json") for thread_num in threads_nums)
        reqs = await asyncio.gather(*tasks)
    for thread in reqs:
        thread = thread.json()
        posts = thread['threads'][0]['posts']
        thread_num = posts[0]['num']
        thread_url = f"https://2ch.hk/{board_name}/res/{thread_num}.html"
        thread_subject = posts[0]['subject']
        for post in posts:
            post_videos = [{'link': f"https://2ch.hk{post_file['path']}", 'name': post_file['fullname'], 'thread_num': thread_num} for post_file in post['files'] if post_file.get('fullname') is not None and post_file.get('fullname').split('.')[-1].strip() in videoext]
            data['videos'].extend(post_videos)
        data['threads'].setdefault(thread_num, {'url': thread_url, 'subject': thread_subject})
    return data

def getVideos():
    if not "HEROKUENV" in environ:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    res = asyncio.run(getAllBoardMedia('b'))
    return res
     
