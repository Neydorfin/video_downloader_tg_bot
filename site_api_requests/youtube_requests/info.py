import pytube
import time

from utils.logging import logger


@logger
def get_info_youtube(link: str) -> dict:
    """
        Получает информацию о видео с YouTube.

        Args:
            link (str): Ссылка на видео.

        Returns:
            dict: Информация о видео.
    """

    @logger
    def get_data(height: int) -> None:
        """
            Обновляет информацию о видео для заданного разрешения.

            Args:
                height (int): Разрешение видео.

            Returns:
                None
        """
        if height in heights:
            # Рассчитывает новый размер файла с учетом аудио и видео
            new_file_size = (video.streams.get_by_itag(frmt["itag"]).filesize_mb + audio_size) * 1.5
            # Получает старый размер файла
            old_file_size = data["_".join(("file_size", str(height)))]

            # Если размер файла неизвестен или новый размер меньше старого
            if old_file_size is None or old_file_size > new_file_size:
                # Обновляет данные в словаре
                data["".join(("_", str(height)))] = frmt['url']
                data["_".join(("file_size", str(height)))] = round(new_file_size, 2)

    # Создает объект YouTube для предоставленной ссылки на видео
    video = pytube.YouTube(link)
    channel = pytube.Channel(video.channel_url)
    # Преобразует длительность видео в формат ЧЧ:ММ:СС
    _time = time.strftime("%H:%M:%S", time.gmtime(video.length))
    # Задает разрешения видео, для которых нужно получить информацию
    heights = (240, 360, 480, 1080, 1440, 2160)
    # Инициализирует словарь с данными о видео
    data = {
        "video_id": video.video_id,
        "title": video.title,
        "time": _time,
        "author": channel.channel_name,
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
    # Инициализирует размер аудио
    audio_size = 1

    # Перебирает форматы аудио для нахождения размера файла аудио
    for frmt in video.streaming_data['adaptiveFormats']:
        tag = frmt["itag"]
        if tag == 140:
            audio_size = round(video.streams.get_by_itag(140).filesize_mb, 2)
            data["audio"] = frmt["url"]

    # Перебирает форматы видео для нахождения размеров файлов
    for frmt in video.streaming_data['formats']:
        tag = frmt["itag"]
        if tag == 22:
            data["_720"] = frmt["url"]
            data["file_size_720"] = round(video.streams.get_by_itag(22).filesize_mb, 2)

    # Если видео сжато в формат "shorts", используются альтернативные форматы
    if "shorts" in link:
        for frmt in video.streaming_data['adaptiveFormats']:
            height = frmt.get('width')
            get_data(height)
    else:
        for frmt in video.streaming_data['adaptiveFormats']:
            height = frmt.get('height')
            get_data(height)
    # Возвращает собранные данные о видео
    return data
