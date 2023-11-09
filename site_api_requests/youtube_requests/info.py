from pytube import YouTube
import time


def get_info_youtube(link):
    def get_data(height):
        if height in heights:
            new_file_size = video.streams.get_by_itag(frmt["itag"]).filesize_mb + audio_size
            old_file_size = data["_".join(("file_size", str(height)))]

            if old_file_size is None or old_file_size > new_file_size:
                data["".join(("_", str(height)))] = frmt['url']
                data["_".join(("file_size", str(height)))] = round(new_file_size, 2)
                print(f"{height} | {frmt['averageBitrate']} |"
                      f" {audio_size} | {data['_'.join(('file_size', str(height)))]}")

    video = YouTube(link)
    _time = time.strftime("%H:%M:%S", time.gmtime(video.length))
    heights = [240, 360, 480, 1080, 1440, 2160]
    data = {
        "video_id": video.video_id,
        "title": video.title,
        "time": _time,
        "time_sec": video.length,
        "thumbnail": video.thumbnail_url,
        "audio": None,  # audio
        "_240": None,  # 240p
        "file_size_240": None,  # 240p file_size
        "_360": None,  # 360p
        "file_size_360": None,  # 360p file_size
        "_480": None,  # 480p
        "file_size_480": None,  # 480p file_size
        "_720": None,  # 720p
        "file_size_720": None,  # 720p file_size
        "_1080": None,  # 1080p
        "file_size_1080": None,  # 1080p file_size
        "_1440": None,  # 1440p
        "file_size_1440": None,  # 1440p file_size
        "_2160": None,  # 2160p
        "file_size_2160": None,  # 2160p file_size
        "video_views": video.views,
    }

    audio_size = 1
    for frmt in video.streaming_data['adaptiveFormats']:
        tag = frmt["itag"]
        if tag == 140:
            audio_size = round(video.streams.get_by_itag(140).filesize_mb, 2)
            data["audio"] = frmt["url"]
    print(audio_size)
    for frmt in video.streaming_data['formats']:
        tag = frmt["itag"]
        if tag == 22:
            data["_720"] = frmt["url"]
            data["file_size_720"] = round(video.streams.get_by_itag(22).filesize_mb, 2)

    if "shorts" in link:
        for frmt in video.streaming_data['adaptiveFormats']:
            height = frmt.get('width')
            get_data(height)
    else:
        for frmt in video.streaming_data['adaptiveFormats']:
            height = frmt.get('height')
            get_data(height)

    return data
