class TeleText:
    welcome: str = "Привет {name}, я бот который поможет тебе в скачивание видео"

    main: str = ("Чтобы начать скачивать видео используй команду /download\n"
                 "Если возникли проблемы используй команду /help")

    help: str = ("Если вы находитесь здесь то у вас появились какие-то вопросы по поводу использование бота\n"
                 "/download - начать скачивание видео\n"
                 "/low - скачать видео в плохом разрешение (240p)\n"
                 "/high - скачать видео в хорошем разрешение (720p)\n"
                 "/default - скачать видео в обычном разрешение (720p)\n"
                 "/custom - настройка таких команд как /low, /high, /info ")

    custom: str = ("Вы решили изменить настройкт при скачивание видео\nИспользуйте выбраные команды:\n"
                   "/low - если хотите изменить минимальное для скачивание видео, разрешение (выбрать из предложенных)\n"
                   "/high - если хотите изменить максимальное для скачивание видео, разрешение (выбрать из предложенных)\n"
                   "/info - если вам не интересует информацио об видео вы можете его просто выкличить\n"
                   "/cancel - выход в меню")
    custom_low: str = "Выберите минимальное разрешение для скачивание видео"
    custom_low_set: str = "Установленное минимальное разрешение для скачивание видео {res}"
    custom_high: str = "Выберите минимальное максимальное для скачивание видео"
    custom_high_set: str = "Установленное максимальное разрешение для скачивание видео {res}"
    custom_info: str = "Если вы хотите получать информацию об видео вкл. эту опцию если нет то выкл."
    custom_info_set: str = "Вы {swith} получение дополнительной информацией об видео!"
    error_custom: str = "Не удалось установить выбраные настройки!"
    platform_select: str = "Выберите откуда вы хотите скачать видео: "
    video_select: str = "Введите ссылку на видео:"
    resolution_select: str = ("Выберите разрешение:\n"
                              "/low\n"
                              "/high\n"
                              "/default\n"
                              "/cancel")
    low: str = "Выбранно минимальное разрешение для скачивание видео"
    high: str = "Выбранно максимальное разрешение для скачивание видео"
    default: str = "Выбранно обычное разрешение для скачивание видео"
    about_video: str = "Назвние: [{title}]({img})\nДлина видео: {time}"
    answer_video: str = "Это ваше видео?"
    start_download: str = "Начало скачивание"
    video_processing: str = "Видео обрабатывается"
    sending_video: str = "Видео отправленно"
    cancel: str = "Назад в меню"
