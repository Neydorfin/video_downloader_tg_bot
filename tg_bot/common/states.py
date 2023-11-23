from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    """
        Определение состояний для обработки диалоговых шагов в телеграм-боте.

        States:
        - main: Главное состояние.
        - custom: Настройка пользовательских параметров.
        - custom_low: Установка нижнего порога.
        - custom_high: Установка верхнего порога.
        - custom_info: Получение информации о пользовательских параметрах.
        - platform_select: Выбор платформы (YouTube/Coub).
        - video_select: Выбор видео.
        - resolution_select: Выбор разрешения видео.
        - about_video: Получение информации о выбранном видео.
        - download: Запуск процесса загрузки видео.
        - video_maker: Создание видео с аудиодорожкой.
        - send_video: Отправка видео в чат.
    """
    main = State()
    custom = State()
    custom_low = State()
    custom_high = State()
    custom_info = State()
    platform_select = State()
    video_select = State()
    resolution_select = State()
    about_video = State()
    download = State()
    video_maker = State()
    send_video = State()
