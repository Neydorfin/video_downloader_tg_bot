from config import COUB_HOST_API
import requests


def pars_link(link: str):
    # https://coub.com/view/3d0s3s
    return link.split('/')[-1]


def get_info_coub(link):
    video_id = pars_link(link)
    url = "/".join((COUB_HOST_API, video_id))
    print(url)
    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'aaaaaemai123@mail.com'  # This is another valid field
    }
    response = requests.get(url=url, headers=headers)
    print(response)
    video_data = response.json()
    video_360p_size = round((video_data["file_versions"]["html5"]["video"]["med"]["size"] +
                             video_data["file_versions"]["html5"]["audio"]["high"]["size"]) / 1_000_000, 2)

    video_720p_size = round((video_data["file_versions"]["html5"]["video"]["high"]["size"] +
                             video_data["file_versions"]["html5"]["audio"]["high"]["size"]) / 1_000_000, 2)
    data = {
        "video_id": video_id,
        "title": video_data["title"],
        "time": video_data["duration"],
        "thumbnail": video_data["picture"],
        "audio": video_data["file_versions"]["html5"]["audio"]["high"]["url"],  # audio
        "_240": None,  # 240p
        "file_size_240": None,  # 240p file_size
        "_360": video_data["file_versions"]["html5"]["video"]["med"]["url"],  # 360p
        "file_size_360": video_360p_size,  # 360p file_size
        "_480": None,  # 480p
        "file_size_480": None,  # 480p file_size
        "_720": video_data["file_versions"]["html5"]["video"]["high"]["url"],  # 720p
        "file_size_720": video_720p_size,  # 720p file_size
        "_1080": None,  # 1080p
        "file_size_1080": None,  # 1080p file_size
        "_1440": None,  # 1440p
        "file_size_1440": None,  # 1440p file_size
        "_2160": None,  # 2160p
        "file_size_2160": None,  # 2160p file_size
        "video_views": video_data["views_count"],
    }

    return data
