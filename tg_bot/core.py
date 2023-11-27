import telebot
from telebot.types import Message, CallbackQuery
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from config import BotSettings
from tg_bot.common.states import States
from tg_bot.common.text import TeleText
from tg_bot.utils.keyboard import Buttons
from database.core import DataBase
from site_api_requests.core import SiteRequests
from video_procesing.video_combine_audio import VideoMaker

# Создание экземпляра StateMemoryStorage для хранения состояний пользователя в памяти
state_storage = StateMemoryStorage()
# Создание экземпляра класса TeleBot из библиотеки python-telegram-bot
# Он инициализируется токеном бота Telegram, полученным из модуля BotSettings
# и экземпляром StateMemoryStorage для управления состояниями пользователя
bot = telebot.TeleBot(BotSettings.BOT_TOKEN, state_storage=state_storage)


@bot.callback_query_handler(func=lambda call: True)
def to_main(call: CallbackQuery) -> None:
    """
        Обработчик для кнопки "Отмена" на клавиатуре. Возвращается в главное меню.
    """
    if call.data == "cancel":
        bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
        main(call.message)


# МЕНЮ
@bot.message_handler(state="*", commands=['main'])
def main(message: Message) -> None:
    """
        Обработчик команды /main

        Аргументы:
            message (Message): Объект входящего сообщения.

        Возвращает:
            None
        """
    # Отправляет основной текст сообщения пользователю и удаляет любые пользовательские кнопки клавиатуры
    bot.send_message(message.chat.id, TeleText.main, reply_markup=Buttons.remove)


# команда запуска бота
@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    """
       Обработчик команды /start.

       Аргументы:
           message (Message): Объект входящего сообщения.

       Возвращает:
           None
       """
    # Проверяет, существует ли пользователь в базе данных, и если нет, добавляет его.
    user = DataBase.read(DataBase.db, DataBase.models.User, message.from_user.id)
    if user is None:
        user_data = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "chat_id": message.chat.id,
        }
        config_data = {
            "user_id": message.from_user.id,
            "low": 240,
            "high": 1080,
            "info": True,
        }
        DataBase.write(DataBase.db, DataBase.models.User, user_data)
        DataBase.write(DataBase.db, DataBase.models.UserConfig, config_data)
    # Отправляет приветственное сообщение и переводит пользователя в состояние 'main'
    bot.send_message(message.chat.id, TeleText.welcome.format(name=message.from_user.first_name),
                     reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


# команда вызова помощи
@bot.message_handler(state="*", commands=['help'])
def help_command(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.help, reply_markup=Buttons.remove)
    main(message)


# команда вызова настроек
@bot.message_handler(commands=['custom'])
def custom(message: Message) -> None:
    """
        Обработчик команды /help.

        Аргументы:
            message (Message): Объект входящего сообщения.

        Возвращает:
            None
        """
    # Отправляет сообщение с информацией о командах и возвращает пользователя в состояние 'main'
    bot.send_message(message.chat.id, TeleText.custom, reply_markup=Buttons.cancel_markup)
    bot.set_state(message.from_user.id, States.custom, message.chat.id)


# команда выбора минимального разрешение видео
@bot.message_handler(state=States.custom, commands=['low'])
def custom_low(message: Message) -> None:
    """
    Обработчик команды /low в состоянии 'custom'.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Отправляет сообщение с инструкциями и клавиатурой для выбора минимального разрешения
    bot.send_message(message.chat.id, TeleText.custom_low, reply_markup=Buttons.low_markup)
    # Устанавливает состояние пользователя в 'custom_low'
    bot.set_state(message.from_user.id, States.custom_low, message.chat.id)


# установка минимального разрешение видео
@bot.message_handler(state=States.custom_low)
def set_low_setting(message: Message) -> None:
    """
    Обработчик сообщений в состоянии 'custom_low'.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Проверка, что текст сообщения находится в списке допустимых разрешений
    if message.text in ["240p", "360p", "480p"]:
        # Обновление настроек пользователя в базе данных
        DataBase.update(DataBase.db, DataBase.models.UserConfig, {"low": message.text}, message.from_user.id)
        # Отправка подтверждения пользователю
        bot.send_message(message.chat.id, TeleText.custom_low_set.format(res=message.text), reply_markup=Buttons.remove)
    else:
        # Отправка сообщения об ошибке, если разрешение не в списке
        bot.send_message(message.chat.id, TeleText.error_custom, reply_markup=Buttons.remove)
    # Переход к обработчику 'custom'
    custom(message)


# команда выбора максимального разрешение видео
@bot.message_handler(state=States.custom, commands=['high'])
def custom_high(message: Message) -> None:
    """
    Обработчик команды '/high' в состоянии 'custom'.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Отправка сообщения пользователю с запросом выбора максимального разрешения
    bot.send_message(message.chat.id, TeleText.custom_high, reply_markup=Buttons.high_markup)
    # Установка состояния 'custom_high' для пользователя
    bot.set_state(message.from_user.id, States.custom_high, message.chat.id)


# установка максимального разрешение видео
@bot.message_handler(state=States.custom_high)
def set_high_setting(message: Message) -> None:
    """
    Обработчик выбора пользователем максимального разрешения в состоянии 'custom_high'.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Проверка, является ли текст сообщения одним из поддерживаемых максимальных разрешений
    if message.text in ["1080p", "1440p", "2160p"]:
        # Обновление настроек пользователя в базе данных
        DataBase.update(DataBase.db, DataBase.models.UserConfig, {"high": message.text}, message.from_user.id)
        # Отправка сообщения о успешном установлении максимального разрешения
        bot.send_message(message.chat.id, TeleText.custom_high_set.format(res=message.text),
                         reply_markup=Buttons.remove)
    else:
        # Отправка сообщения об ошибке при некорректном вводе
        bot.send_message(message.chat.id, TeleText.error_custom, reply_markup=Buttons.remove)
    # Возврат пользователя в основное меню 'custom'
    custom(message)


# команда по поводу получение доп. информации про выидео
@bot.message_handler(state=States.custom, commands=['info'])
def custom_info(message: Message) -> None:
    """
    Обработчик команды /info в состоянии 'custom'.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Отправка сообщения с вопросом о настройке получения информации об видео
    bot.send_message(message.chat.id, TeleText.custom_info, reply_markup=Buttons.switch_markup)
    # Установка состояния 'custom_info' для пользователя
    bot.set_state(message.from_user.id, States.custom_info, message.chat.id)


# установка настроек доп. информации про выидео
@bot.message_handler(state=States.custom_info)
def set_info_setting(message: Message) -> None:
    """
    Обработчик установки настройки получения информации об видео в состоянии 'custom_info'.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Словарь для сопоставления текстовых ответов пользователя с булевыми значениями
    set_info_dict = {
        "ВКЛ": True,
        "ВЫКЛ": False,
    }
    # Проверка, что текст сообщения пользователя валиден
    if message.text in set_info_dict:
        # Обновление настройки в базе данных
        DataBase.update(DataBase.db, DataBase.models.UserConfig, {"info": set_info_dict[message.text]},
                        message.from_user.id)
        # Отправка подтверждения установки настройки и удаление клавиатуры
        bot.send_message(message.chat.id, TeleText.custom_info_set.format(swith=message.text),
                         reply_markup=Buttons.remove)
    else:
        # Отправка сообщения об ошибке в случае невалидного ввода
        bot.send_message(message.chat.id, TeleText.error_custom, reply_markup=Buttons.remove)
    # Переход обратно в состояние 'custom'
    custom(message)


# команда отмены
@bot.message_handler(state="*", commands=['cancel'])
def cancel(message: Message) -> None:
    """
    Обработчик команды отмены в любом состоянии.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Отправка сообщения об отмене и удаление клавиатуры
    bot.send_message(message.chat.id, TeleText.cancel, reply_markup=Buttons.remove)
    # Сброс состояния пользователя в 'main' и вызов соответствующего обработчика
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


@bot.message_handler(state=States.main, commands=['history'])
def history(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.history_questions, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.history, message.chat.id)


@bot.message_handler(state=States.history)
def history_print(message: Message) -> None:
    queries = DataBase.read(DataBase.db, DataBase.models.History, message.from_user.id, limit=message.text)
    user_config = DataBase.read(DataBase.db, DataBase.models.UserConfig, message.from_user.id)
    for record in queries:
        if user_config.info:
            bot.send_photo(message.chat.id, record.thumbnail,
                           caption=TeleText.history_video_info
                           .format(title=record.title, time=record.time,
                                   author=record.author, views=record.video_views,
                                   date=record.created_at, link=record.link),
                           parse_mode='Markdown')
        else:
            bot.send_photo(message.chat.id, record.thumbnail,
                           caption=TeleText.history_video
                           .format(title=record.title, date=record.created_at, link=record.link),
                           parse_mode='Markdown')
    cancel(message)


# пользователь выбирает платформу с которой он будет скачивать видео
@bot.message_handler(state=States.main, commands=['download'])
def platform_select(message: Message) -> None:
    """
    Обработчик команды выбора платформы для скачивания видео в основном состоянии.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Отправка сообщения о выборе платформы и клавиатуры с вариантами
    bot.send_message(message.chat.id, TeleText.platform_select, reply_markup=Buttons.platform_markup)
    # Установка состояния пользователя в 'platform_select'
    bot.set_state(message.from_user.id, States.platform_select, message.chat.id)


# читаем ссылку от пользователя
@bot.message_handler(state=States.platform_select)
def video_select(message: Message) -> None:
    """
    Обработчик выбора платформы для скачивания видео в состоянии выбора платформы.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    if message.text not in ["YouTube", "Coub"]:  # , "Vk"
        # Отправка сообщения об ошибке выбора платформы и удаление клавиатуры
        bot.send_message(message.chat.id, TeleText.error_platform, reply_markup=Buttons.remove)
        # Вызов обработчика отмены
        cancel(message)
    else:
        # Создание данных для записи в историю
        data = {
            "user_id": message.from_user.id,
            "platform": message.text,
        }
        # Запись данных в базу данных
        DataBase.write(DataBase.db, DataBase.models.History, data=data)
        # Отправка сообщения о выборе видео и удаление клавиатуры
        bot.send_message(message.chat.id, TeleText.video_select, reply_markup=Buttons.remove)
        # Установка состояния пользователя в 'video_select'
        bot.set_state(message.from_user.id, States.video_select, message.chat.id)


# выво информации об видео с вопросом о продолжение скачивание
@bot.message_handler(state=States.video_select)
def about_video(message: Message) -> None:
    """
    Обработчик получения информации о видео в состоянии выбора видео.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    error = False
    # Чтение данных о текущей сессии и настройках пользователя из базы данных
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    user_config = DataBase.read(DataBase.db, DataBase.models.UserConfig, user_id=message.from_user.id)
    data = {}

    # Попытка получить информацию о видео в зависимости от выбранной платформы
    if session.platform == "YouTube":
        try:
            data = SiteRequests.YouTube.get_info_youtube(message.text)
        except:
            bot.reply_to(message, text=TeleText.error_video)
            error = True
    elif session.platform == "Coub":
        try:
            data = SiteRequests.Coub.get_info_coub(message.text)
        except:
            bot.reply_to(message, text=TeleText.error_video)
            error = True

    if not error:
        # Отправка информации о видео с учетом настроек пользователя
        if user_config.info:
            bot.send_message(message.chat.id, text=TeleText.about_video_info
                             .format(title=data["title"], time=data["time"],
                                     author=data["author"], views=data["video_views"],
                                     img=data['thumbnail']),
                             parse_mode='Markdown', reply_to_message_id=message.id)
        else:
            bot.send_message(message.chat.id, text=TeleText.about_video
                             .format(title=data["title"], time=data["time"],
                                     img=data['thumbnail']),
                             parse_mode='Markdown', reply_to_message_id=message.id)

        data.update({"link": message.text})

        # Обновление информации о видео в базе данных и переход в следующее состояние
        DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)
        bot.send_message(message.chat.id, TeleText.answer_video, reply_markup=Buttons.answer_markup)
        bot.set_state(message.from_user.id, States.about_video, message.chat.id)
    else:
        # Ошибка, возврат в главное меню
        cancel(message)


@bot.message_handler(state=States.about_video)  # выбор разрешение видео
def resolution_select(message: Message) -> None:
    """
    Обработчик выбора разрешения видео после предоставления информации о видео.

    Аргументы:
        message (Message): Объект входящего сообщения.

    Возвращает:
        None
    """
    # Чтение данных о текущей сессии и настройках пользователя из базы данных
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    user_config = DataBase.read(DataBase.db, DataBase.models.UserConfig, user_id=message.from_user.id)

    # Проверка выбора пользователя
    if message.text == "Нет":
        cancel(message)
    else:
        # Отправка сообщения с возможными разрешениями видео и переход в следующее состояние
        if session.platform == "YouTube":
            bot.send_message(message.chat.id, TeleText.resolution_select
                             .format(low_res=user_config.low,
                                     low=getattr(session, "_".join(("file_size", str(user_config.low)))),
                                     high_res=user_config.high,
                                     high=getattr(session, "_".join(("file_size", str(user_config.high)))),
                                     default=session.file_size_720), reply_markup=Buttons.remove)
        elif session.platform == "Coub":
            bot.send_message(message.chat.id, TeleText.resolution_select
                             .format(low_res=360,
                                     low=session.file_size_360,
                                     high_res=720,
                                     high=session.file_size_720,
                                     default=session.file_size_720), reply_markup=Buttons.remove)
        bot.set_state(message.from_user.id, States.resolution_select, message.chat.id)


@bot.message_handler(state=States.resolution_select, commands=['low'])  # выбор минимального разрешение
def low(message: Message) -> None:
    """
        Данный обработчик вызывается при команде /low в состоянии выбора разрешения видео.

        Аргументы:
            message (Message): Объект входящего сообщения.

        Возвращает:
            None
    """
    # Получаем данные пользователя из базы данных
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    user_config = DataBase.read(DataBase.db, DataBase.models.UserConfig, user_id=message.from_user.id)

    # Инициализируем словарь для обновления данных
    data = dict()

    # В зависимости от выбранной платформы устанавливаем соответствующее разрешение
    if session.platform == "YouTube":
        data = {
            "resolution": user_config.low,
        }
    elif session.platform == "Coub":
        data = {
            "resolution": 360,
        }

    # Обновляем данные в базе данных
    DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)

    # Отправляем сообщение о выборе минимального разрешения и переводим пользователя в следующее состояние
    bot.send_message(message.chat.id, TeleText.low, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.video_maker, message.chat.id)
    video_maker(message)


# выбор максимального разрешение
@bot.message_handler(state=States.resolution_select, commands=['high'])
def high(message: Message) -> None:
    """
        Обработчик вызывается при команде /high в состоянии выбора разрешения видео.

        Аргументы:
            message (Message): Объект входящего сообщения.

        Возвращает:
            None
    """
    # Получаем данные пользователя из базы данных
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    user_config = DataBase.read(DataBase.db, DataBase.models.UserConfig, user_id=message.from_user.id)

    # Инициализируем словарь для обновления данных
    data = dict()

    # В зависимости от выбранной платформы устанавливаем соответствующее разрешение
    if session.platform == "YouTube":
        data = {
            "resolution": user_config.high,
        }
    elif session.platform == "Coub":
        data = {
            "resolution": 720,
        }

    # Обновляем данные в базе данных
    DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)

    # Отправляем сообщение о выборе максимального разрешения и переводим пользователя в следующее состояние
    bot.send_message(message.chat.id, TeleText.high, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.video_maker, message.chat.id)
    video_maker(message)


# выбор разрешение по умолчанию
@bot.message_handler(state=States.resolution_select, commands=['default'])
def default(message: Message) -> None:
    """
        Обработчик вызывается при команде /default в состоянии выбора разрешения видео.

        Аргументы:
            message (Message): Объект входящего сообщения.

        Возвращает:
            None
    """
    # Получаем данные пользователя из базы данных
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)

    # В зависимости от выбранной платформы устанавливаем разрешение по умолчанию
    if session.platform == "YouTube":
        data = {
            "resolution": 720,
        }
        # Обновляем данные в базе данных
        DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)
        # Отправляем сообщение о выборе разрешения по умолчанию и переводим пользователя в следующее состояние
        bot.send_message(message.chat.id, TeleText.default, reply_markup=Buttons.remove)
        bot.set_state(message.from_user.id, States.download, message.chat.id)
        download(message)
    elif session.platform == "Coub":
        data = {
            "resolution": 720,
        }
        # Обновляем данные в базе данных
        DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)
        # Отправляем сообщение о выборе разрешения по умолчанию и переводим пользователя в следующее состояние
        bot.send_message(message.chat.id, TeleText.default, reply_markup=Buttons.remove)
        bot.set_state(message.from_user.id, States.video_maker, message.chat.id)
        video_maker(message)


# скачивание видео
@bot.message_handler(state=States.download)
def download(message: Message) -> None:
    """
        Обработчик вызывается в состоянии скачивания видео.

        Аргументы:
            message (Message): Объект входящего сообщения.

        Возвращает:
            None
    """
    # Получаем данные пользователя из базы данных
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)

    # Отправляем сообщение о начале скачивания
    bot.send_message(message.chat.id, TeleText.start_download, reply_markup=Buttons.remove)

    # В зависимости от выбранной платформы вызываем соответствующую функцию скачивания
    if session.platform == "YouTube":
        SiteRequests.YouTube.default_download(session)

    # Переводим пользователя в следующее состояние
    bot.set_state(message.from_user.id, States.send_video, message.chat.id)
    send_video(message)


# обработка видео
@bot.message_handler(state=States.video_maker)
def video_maker(message: Message) -> None:
    """
        Обработчик для состояния создания видео.

        Аргументы:
            message (Message): Объект входящего сообщения.

        Возвращает:
            None
    """
    # Получаем данные пользователя из базы данных
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    bot.send_message(message.chat.id, TeleText.video_processing, reply_markup=Buttons.remove)
    resolution = session.resolution
    video = getattr(session, "".join(("_", resolution)))
    try:
        # Попытка объединить аудио и видео в один файл
        VideoMaker.combine_audio(video, session.audio, session.video_id)
    except:
        # Обработка ошибки: отправка сообщения об ошибке и перевод пользователя в состояние отмены
        bot.send_message(message.chat.id, TeleText.error_video_maker, reply_markup=Buttons.remove)
        cancel(message)
    else:
        # Если успешно, перевод пользователя в состояние отправки видео
        bot.set_state(message.from_user.id, States.send_video, message.chat.id)
        send_video(message)


# отправка видео
@bot.message_handler(state=States.send_video)
def send_video(message: Message) -> None:
    """
        Обработчик для состояния отправки видео.

        Параметры:
            message (telebot.types.Message): Объект сообщения от пользователя.

        Логика:
        1. Получает данные пользователя из базы данных.
        2. Пытается отправить видео в чат.
        3. В случае ошибки отправляет сообщение об ошибке и переводит пользователя в состояние отмены.
        4. Если успешно, отправляет сообщение о завершении и переводит пользователя в главное состояние.

        Примечание:
            Замените 'cancel(message)' на реальную функцию обработки, если она отличается от вашей.
    """
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    try:
        # Пытается отправить видео в чат
        bot.send_video(message.chat.id, open(f"resources/video/{session.video_id}.mp4", "rb"))
    except:
        # Обработка ошибки: отправка сообщения об ошибке и перевод пользователя в состояние отмены
        bot.send_message(message.chat.id, TeleText.error_sending_video, reply_markup=Buttons.remove)
        VideoMaker.delete_video(session)
        cancel(message)
    else:
        # Если успешно, отправка сообщения о завершении и перевод пользователя в главное состояние
        bot.send_message(message.chat.id, TeleText.sending_video, reply_markup=Buttons.remove)
        VideoMaker.delete_video(session)
        cancel(message)


def run():
    """
        Запуск бота.

        Примечание:
            Замените команды на свои, если они отличаются от приведенных.
    """
    # Добавляет фильтр состояния для обработчиков
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    # Устанавливает пользовательские команды бота
    bot.set_my_commands([
        telebot.types.BotCommand("start", "Запуск бота"),
        telebot.types.BotCommand("help", "Помощь по боту"),
        telebot.types.BotCommand("custom", "Настройка бота"),
        telebot.types.BotCommand("history", "История запросов"),
        telebot.types.BotCommand("download", "Начать скачивать видео"),
        telebot.types.BotCommand("cancel", "Назад в Меню"),
    ])
    # Запускает бота на получение обновлений
    bot.polling()


if __name__ == '__main__':
    run()
