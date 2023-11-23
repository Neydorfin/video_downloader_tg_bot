from pytube import YouTube
from database.core import DataBase


def default_download(data: DataBase.models.History) -> None:
    """
        Скачивает видео с YouTube в наивысшем разрешении.

        Args:
            data (History): Информация о видео.

        Returns:
            None
    """
    video = YouTube(data.link)
    youtube_object = video.streams.get_highest_resolution()
    try:
        youtube_object.download(output_path="resources/video", filename=f"{data.video_id}.mp4")
    except:
        print("An error has occurred")
        return
    print("Download is completed successfully")
