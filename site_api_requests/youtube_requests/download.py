from pytube import YouTube


def default_download(data) -> None:
    video = YouTube(data.link)
    youtube_object = video.streams.get_highest_resolution()
    try:
        youtube_object.download(output_path="resources/video", filename=f"{data.video_id}.mp4")
    except:
        print("An error has occurred")
        return
    print("Download is completed successfully")
