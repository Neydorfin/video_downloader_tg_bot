from site_api_requests.youtube_requests.info import get_info_youtube
from site_api_requests.youtube_requests.download import default_download
from site_api_requests.coub_requests.info import get_info_coub


class YouTube:
    """
    Класс, предоставляющий методы для работы с YouTube.
    """
    get_info_youtube = get_info_youtube
    default_download = default_download


class Coub:
    """
    Класс, предоставляющий методы для работы с Coub.
    """
    get_info_coub = get_info_coub


class SiteRequests:
    """
    Класс, объединяющий методы для работы с различными сайтами.
    """
    YouTube = YouTube
    Coub = Coub
