import time

import telebot
from telebot.types import Message, CallbackQuery
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from config import BotSettings
from tg_bot.common.states import States
from tg_bot.common.text import TeleText
from tg_bot.utils.keyboard import Buttons
from database.core import DataBase
from site_api_requests.youtube_requests.info import get_info_youtube
from site_api_requests.youtube_requests.download import default_download

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BotSettings.BOT_TOKEN, state_storage=state_storage)


@bot.callback_query_handler(func=lambda call: True)
def to_main(call: CallbackQuery) -> None:
    if call.data == "cancel":
        bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
        main(call.message)


# МЕНЮ
@bot.message_handler(state=States.main, commands=['main'])
def main(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.main, reply_markup=Buttons.remove)


# команда запуска бота
@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
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
    bot.send_message(message.chat.id, TeleText.custom, reply_markup=Buttons.cancel_markup)
    bot.set_state(message.from_user.id, States.custom, message.chat.id)


# команда выбора минимального разрешение видео
@bot.message_handler(state=States.custom, commands=['low'])
def custom_low(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_low, reply_markup=Buttons.low_markup)
    bot.set_state(message.from_user.id, States.custom_low, message.chat.id)


# установка минимального разрешение видео
@bot.message_handler(state=States.custom_low)
def set_low_setting(message: Message) -> None:
    if message.text in ["240p", "360p", "480p"]:
        DataBase.update(DataBase.db, DataBase.models.UserConfig, {"low": message.text}, message.from_user.id)
        bot.send_message(message.chat.id, TeleText.custom_low_set.format(res=message.text), reply_markup=Buttons.remove)
    else:
        bot.send_message(message.chat.id, TeleText.error_custom, reply_markup=Buttons.remove)
    custom(message)


# команда выбора максимального разрешение видео
@bot.message_handler(state=States.custom, commands=['high'])
def custom_high(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_high, reply_markup=Buttons.high_markup)
    bot.set_state(message.from_user.id, States.custom_high, message.chat.id)


# установка максимального разрешение видео
@bot.message_handler(state=States.custom_high)
def set_high_setting(message: Message) -> None:
    if message.text in ["1080p", "1440p", "2160p"]:
        DataBase.update(DataBase.db, DataBase.models.UserConfig, {"high": message.text}, message.from_user.id)
        bot.send_message(message.chat.id, TeleText.custom_high_set.format(res=message.text),
                         reply_markup=Buttons.remove)
    else:
        bot.send_message(message.chat.id, TeleText.error_custom, reply_markup=Buttons.remove)
    custom(message)


# команда по поводу получение доп. информации про выидео
@bot.message_handler(state=States.custom, commands=['info'])
def custom_info(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_info, reply_markup=Buttons.switch_markup)
    bot.set_state(message.from_user.id, States.custom_info, message.chat.id)


# установка настроек доп. информации про выидео
@bot.message_handler(state=States.custom_info)
def set_info_setting(message: Message) -> None:
    set_info_dict = {
        "ВКЛ": True,
        "ВЫКЛ": False,
    }
    if message.text in ["ВКЛ", "ВЫКЛ"]:
        DataBase.update(DataBase.db, DataBase.models.UserConfig, {"info": set_info_dict[message.text]},
                        message.from_user.id)
        bot.send_message(message.chat.id, TeleText.custom_info_set.format(swith=message.text),
                         reply_markup=Buttons.remove)
    else:
        bot.send_message(message.chat.id, TeleText.error_custom, reply_markup=Buttons.remove)
    custom(message)


# команда отмены
@bot.message_handler(state="*", commands=['cancel'])
def cancel(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.cancel, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


# пользователь выбирает платформу с которой он будет скачивать видео
@bot.message_handler(state=States.main, commands=['download'])
def platform_select(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.platform_select, reply_markup=Buttons.platform_markup)
    bot.set_state(message.from_user.id, States.platform_select, message.chat.id)


# читаем ссылку от пользователя
@bot.message_handler(state=States.platform_select)
def video_select(message: Message) -> None:
    data = {
        "user_id": message.from_user.id,
        "platform": message.text,
    }
    DataBase.write(DataBase.db, DataBase.models.History, data=data)
    bot.send_message(message.chat.id, TeleText.video_select, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.video_select, message.chat.id)


# выво информации об видео с вопросом о продолжение скачивание
@bot.message_handler(state=States.video_select)
def about_video(message: Message) -> None:
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    print(session)
    data = {}
    if session.platform == "YouTube":
        data = get_info_youtube(message.text)
    # elif session.platform == "Vk":
    #     data = get_info_vk(message.text)
    # elif session.platform == "Coub":
    #     data = get_info_coub(message.text)
    else:
        bot.send_message(message.chat.id, TeleText.error_platform, reply_markup=Buttons.remove)
        cancel(message)
    bot.reply_to(message,
                 text=TeleText.about_video.format(img=data["thumbnail"], title=data["title"],
                                                  time=data["time"]),
                 parse_mode='Markdown')
    data.update({"link": message.text})

    DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)
    bot.send_message(message.chat.id, TeleText.answer_video, reply_markup=Buttons.answer_markup)
    bot.set_state(message.from_user.id, States.about_video, message.chat.id)


# выбор разрешение видео
@bot.message_handler(state=States.about_video)
def resolution_select(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.resolution_select, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.resolution_select, message.chat.id)


# выбор минимального разрешение
@bot.message_handler(state=States.resolution_select, commands=['low'])
def low(message: Message) -> None:
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    data = {
        "resolution": "low",
    }
    DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)
    bot.send_message(message.chat.id, TeleText.low, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


# выбор максимального разрешение
@bot.message_handler(state=States.resolution_select, commands=['high'])
def high(message: Message) -> None:
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    data = {
        "resolution": "high",
    }
    DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)
    bot.send_message(message.chat.id, TeleText.high, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


# выбор разрешение по умолчанию
@bot.message_handler(state=States.resolution_select, commands=['default'])
def default(message: Message) -> None:
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    data = {
        "resolution": "default",
    }
    DataBase.update(DataBase.db, DataBase.models.History, data=data, user_id=session)
    bot.send_message(message.chat.id, TeleText.default, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


# скачивание видео
@bot.message_handler(state=States.download)
def download(message: Message) -> None:
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    bot.send_message(message.chat.id, TeleText.start_download, reply_markup=Buttons.remove)
    if session.platform == "YouTube":
        default_download(session)
    bot.set_state(message.from_user.id, States.video_maker, message.chat.id)
    video_maker(message)


# обработка видео
@bot.message_handler(state=States.video_maker)
def video_maker(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.video_processing, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.send_video, message.chat.id)
    send_video(message)


# отправка видео
@bot.message_handler(state=States.send_video)
def send_video(message: Message) -> None:
    session = DataBase.read(DataBase.db, DataBase.models.History, user_id=message.from_user.id)
    bot.send_video(message.chat.id, video=open(f"resources/video/{session.video_id}.mp4", "rb"))
    bot.send_message(message.chat.id, TeleText.sending_video, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


def run():
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.set_my_commands([
        telebot.types.BotCommand("start", "Запуск бота"),
        telebot.types.BotCommand("help", "Помощь по боту"),
        telebot.types.BotCommand("custom", "Настройка бота"),
        telebot.types.BotCommand("download", "Начать скачивать видео"),
        telebot.types.BotCommand("cancel", "Назад в Меню"),
    ])
    bot.polling()


if __name__ == '__main__':
    run()
