from config import COUB_HOST_API
import requests


def pars_link(link: str):
    """
       Получает идентификатор видео из ссылки.

       Args:
           link (str): Ссылка на видео.

       Returns:
           str: Идентификатор видео.
       """
    return link.split('/')[-1]


def get_info_coub(link):
    """
        Получает информацию о видео с Coub.

        Args:
            link (str): Ссылка на видео.

        Returns:
            dict: Информация о видео.
        """
    video_id = pars_link(link)
    url = "/".join((COUB_HOST_API, video_id))
    print(url)
    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'aaaaaemai123@mail.com'
    }
    response = requests.get(url=url, headers=headers)
    print(response)
    video_data = response.json()
    # Вычисление размеров видео для разных разрешений
    video_360p_size = round((video_data["file_versions"]["html5"]["video"]["med"]["size"] +
                             video_data["file_versions"]["html5"]["audio"]["high"]["size"]) / 1_000_000, 2)

    video_720p_size = round((video_data["file_versions"]["html5"]["video"]["high"]["size"] +
                             video_data["file_versions"]["html5"]["audio"]["high"]["size"]) / 1_000_000, 2)
    data = {
        "video_id": video_id,
        "author": video_data["channel"]["title"],
        "title": video_data["title"],
        "time": video_data["duration"],
        "thumbnail": video_data["picture"],
        "audio": video_data["file_versions"]["html5"]["audio"]["high"]["url"],  # audio
        "_360": video_data["file_versions"]["html5"]["video"]["med"]["url"],  # 360p
        "file_size_360": video_360p_size,  # 360p file_size
        "_720": video_data["file_versions"]["html5"]["video"]["high"]["url"],  # 720p
        "file_size_720": video_720p_size,  # 720p file_size
        "video_views": video_data["views_count"],
    }

    return data
