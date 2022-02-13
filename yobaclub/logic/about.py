from requests import get
from json import load
from datetime import datetime
from os import getenv


def to_timestamp(strtime: str) -> float:
    return datetime.strptime(strtime, r"%Y-%m-%dT%H:%M:%SZ").timestamp()+18000

def remove_links(string: str) -> str:
    words = string.split(" ")
    for i, word in enumerate(words):
        for link_part in ["https:/", "http:/", "www.", ".com"]:
            if link_part in word:
                words[i] = "[ссылка удалена]"
    return ' '.join(words)

def get_commits() -> list:
    if getenv("HEROKU") is not None:
        link = getenv("GIT_LINK")
        token = getenv("GIT_TOKEN")
    else:
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
                        "time": to_timestamp(payload["commit"]["author"]["date"])}
                        for payload in res.json()]
        repo_commits.extend(page_commits)
        if res.links.get("next") is None:
            break
        link = res.links['next']['url']
    return repo_commits