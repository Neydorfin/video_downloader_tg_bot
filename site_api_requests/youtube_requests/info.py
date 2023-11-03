from pytube import YouTube
import time


def get_info(link):
    video = YouTube(link)
    ty_res = time.gmtime(video.length)
    res = time.strftime("%H:%M:%S", ty_res)

    data = {
        "title": video.title,
        "time": res,
        "thumbnail": video.thumbnail_url,
        "info": video.vid_info
    }
    return data
