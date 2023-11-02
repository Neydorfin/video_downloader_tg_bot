import telebot
from telebot.types import Message, CallbackQuery
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from config import BotSettings
from tg_bot.common.states import States
from tg_bot.common.text import TeleText
from tg_bot.utils.keyboard import Buttons

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BotSettings.BOT_TOKEN, state_storage=state_storage)


# МЕНЮ
@bot.message_handler(state=States.main, commands=['main'])
def main(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.main, reply_markup=Buttons.remove)


# команда запуска бота
@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.welcome, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


# команда вызова помощи
@bot.message_handler(state="*", commands=['help'])
def help(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.help, reply_markup=Buttons.remove)


# команда вызова настроек
@bot.message_handler(commands=['custom'])
def custom(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.custom, message.chat.id)


# команда выбора минимального разрешение видео
@bot.message_handler(state=States.custom, commands=['low'])
def custom_low(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_low, reply_markup=Buttons.low_markup)


# команда выбора максимального разрешение видео
@bot.message_handler(state=States.custom, commands=['high'])
def custom_high(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_high, reply_markup=Buttons.high_markup)


# команда по поводу получение доп. информации про выидео
@bot.message_handler(state=States.custom, commands=['info'])
def custom_info(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_info, reply_markup=Buttons.switch_markup)


# команда отмены
@bot.message_handler(state="*", commands=['cancel'])
def cancel(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.cancel, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


# пользователб выбирает платформу с которой он будет скачивать видео
@bot.message_handler(state=States.main, commands=['download'])
def platform_select(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.platform_select, reply_markup=Buttons.platform_markup)
    bot.set_state(message.from_user.id, States.platform_select, message.chat.id)


# читаем ссылку от пользователя
@bot.message_handler(state=States.platform_select)
def video_select(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.video_select, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.video_select, message.chat.id)


# выво информации об видео с вопросом о продолжение скачивание
@bot.message_handler(state=States.video_select)
def about_video(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.about_video, reply_markup=Buttons.answer_markup)
    bot.set_state(message.from_user.id, States.about_video, message.chat.id)


# выбор разрешение видео
@bot.message_handler(state=States.about_video)
def resolution_select(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.resolution_select, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.resolution_select, message.chat.id)


# выбор минимального разрешение
@bot.message_handler(state=States.resolution_select, commands=['low'])
def low(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.low, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


# выбор максимального разрешение
@bot.message_handler(state=States.resolution_select, commands=['high'])
def high(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.high, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


# выбор разрешение по умолчанию
@bot.message_handler(state=States.resolution_select, commands=['default'])
def default(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.default, reply_markup=Buttons.remove)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


# скачивание видео
@bot.message_handler(state=States.download)
def download(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.start_download, reply_markup=Buttons.remove)
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
