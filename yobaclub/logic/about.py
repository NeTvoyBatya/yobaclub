#ВСЕМ ПРИВЕТ, МЕНЯ ЗОВУТ АЛЕКС784 И СЕГОДНЯ Я ПОКАЖУ ВАМ, 
#КАК ПАРСИТЬ ВСЕ КОММИТЫ С ПРИВАТНОГО РЕППОЗИТОРИЯ
from requests import get
from json import load
from datetime import datetime

def process_time(strtime: str) -> str:
    strtime = strtime.replace("Z", "")
    dt = datetime.strptime(strtime, r"%Y-%m-%dT%H:%M:%S")
    strtime = dt.strftime(r"%d.%m.%Y %H:%M:%S")
    return strtime

def remove_links(string: str) -> str:
    words = string.split(" ")
    for i, word in enumerate(words):
        for link_part in ["https:/", "http:/", "www.", ".com"]:
            if link_part in word:
                words[i] = "[ссылка удалена]"
    return ' '.join(words)

def get_commits() -> list:
    with open("secrets.json", 'r', encoding="utf-8") as f:
        secrets = load(f)
    link = secrets["git_link"]
    token = secrets["git_token"]
    login = "NeTvoyBatya"
    repo_commits = []
    
    while True:
        res = get(link, auth=(login, token))
        page_commits = [{"author": payload["author"]["login"] if payload.get("author") is not None 
                            else payload["commit"]["author"]["name"], 
                        "author_img": payload["author"]["avatar_url"] if payload.get("author") is not None
                            else None,
                        "author_link": payload["author"]["html_url"] if payload.get("author") is not None
                            else None,
                        "message": remove_links(payload["commit"]["message"]), 
                        "time": process_time(payload["commit"]["author"]["date"])}
                        for payload in res.json()]
        repo_commits.extend(page_commits)
        if res.links.get("next") is None:
            break
        link = res.links['next']['url']
    return repo_commits