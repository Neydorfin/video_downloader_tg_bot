from site_api_requests.youtube_requests.info import get_info_youtube
from site_api_requests.youtube_requests.download import default_download
from site_api_requests.coub_requests.info import get_info_coub


class YouTube:
    get_info_youtube = get_info_youtube
    default_download = default_download


class Coub:
    get_info_coub = get_info_coub


class SiteRequests:
    YouTube = YouTube
    Coub = Coub
