from subprocess import run
from json import load, loads
from acrcloud.recognizer import ACRCloudRecognizer

def secondsToHumanTime(seconds):
        seconds = round(seconds)
        hours, remain = divmod(seconds, 3600)
        minutes, seconds = divmod(remain, 60)
        time = '{:00}:{:00}:{:00}'.format(int(hours), int(minutes), int(seconds))
        list = time.split(':')
        for i, part in enumerate(list):
            if len(part) == 1:
                list[i] = '0'+part
        time = list[0]+':'+list[1]+':'+list[2]
        return time
        
def cutToRecognize(video_path, start_time, video_duration, output_path=None):
    end_time = start_time+10 if start_time+10 < video_duration else video_duration-1
    start_time_str = secondsToHumanTime(start_time)
    end_time_str = secondsToHumanTime(end_time)
    if output_path is None:
        output_path = video_path[:video_path.rindex('.')]+"-cutted"+video_path[video_path.rindex('.'):]
    result = run(f"ffmpeg -i {video_path} -ss {start_time_str} -to {end_time_str} -map 0:a -c copy {output_path}")
    if result.returncode != 0:
        return None
    return output_path

def recognizeFile(filepath):
    with open("secrets.json", 'r', encoding="utf-8") as f:
        secrets = load(f)
        config = {
        "host": secrets.get("acr_host"),
        "access_key": secrets.get("acr_access_key"),
        "access_secret": secrets.get("acr_secret_key"),
        "timeout": 10
        }
    recognizer = ACRCloudRecognizer(config)
    result = recognizer.recognize_by_file(filepath, 0)
    result = loads(result)
    if result.get("status") is not None:
        if result.get("status").get("code") == 0:
            data = result.get("metadata").get("music")[0]
            return f"{data.get('artists')[0].get('name')} - {data.get('title')}"
    return None
    
    
        
