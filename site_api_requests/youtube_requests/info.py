from pytube import YouTube
import time


def get_info_youtube(link):
    video = YouTube(link)
    _time = time.strftime("%H:%M:%S", time.gmtime(video.length))

    data = {
        "video_id": video.video_id,
        "title": video.title,
        "time": _time,
        "thumbnail": video.thumbnail_url,
        "_140": None,  # audio
        "_242": None,  # 244p
        "_18": None,  # 360p
        "_244": None,  # 480p
        "_22": None,  # 720p
        "_137": None,  # 1080p
        "_271": None,  # 1440p
        "_313": None,  # 2160p
        "video_views": video.views,
    }

    for frmt in video.streaming_data['formats']:
        tag = "".join(("_", str(frmt["itag"])))
        if tag in data.keys():
            data[tag] = frmt['url']

    for frmt in video.streaming_data['adaptiveFormats']:
        tag = "".join(("_", str(frmt["itag"])))
        if tag in data.keys():
            data[tag] = frmt['url']
    return data
