import telebot
from telebot.types import Message
from telebot import custom_filters
from telebot.storage import StateMemoryStorage
from config import BotSettings
from common.states import States
from common.text import TeleText

state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BotSettings.BOT_TOKEN, state_storage=state_storage)


@bot.message_handler(commands=['start'])
def start(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.welcome)
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


@bot.message_handler(state="*", commands=['help'])
def help(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.help)


@bot.message_handler(commands=['custom'])
def custom(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom)
    bot.set_state(message.from_user.id, States.custom, message.chat.id)


@bot.message_handler(state=States.main, commands=[])
def main(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.main)


@bot.message_handler(state=States.custom, commands=['low'])
def custom_low(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_low)


@bot.message_handler(state=States.custom, commands=['high'])
def custom_high(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_high)


@bot.message_handler(state=States.custom, commands=['info'])
def custom_info(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.custom_info)


@bot.message_handler(state=[States.custom, States.resolution_select], commands=['cancel'])
def cancel(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.cancel)
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


@bot.message_handler(state=States.main, commands=['download'])
def start_download(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.platform_select)
    bot.set_state(message.from_user.id, States.platform_select, message.chat.id)


@bot.message_handler(state=States.platform_select)
def platform_select(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.video_select)
    bot.set_state(message.from_user.id, States.video_select, message.chat.id)


@bot.message_handler(state=States.video_select)
def video_select(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.about_video)
    bot.set_state(message.from_user.id, States.about_video, message.chat.id)


@bot.message_handler(state=States.about_video)
def about_video(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.resolution_select)
    bot.set_state(message.from_user.id, States.resolution_select, message.chat.id)


@bot.message_handler(state=States.resolution_select, commands=['low'])
def low(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.low)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


@bot.message_handler(state=States.resolution_select, commands=['high'])
def high(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.high)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


@bot.message_handler(state=States.resolution_select, commands=['default'])
def default(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.default)
    bot.set_state(message.from_user.id, States.download, message.chat.id)
    download(message)


@bot.message_handler(state=States.download)
def download(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.start_download)
    bot.set_state(message.from_user.id, States.video_maker, message.chat.id)
    video_maker(message)


@bot.message_handler(state=States.video_maker)
def video_maker(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.video_processing)
    bot.set_state(message.from_user.id, States.send_video, message.chat.id)
    send_video(message)


@bot.message_handler(state=States.send_video)
def send_video(message: Message) -> None:
    bot.send_message(message.chat.id, TeleText.sending_video)
    bot.set_state(message.from_user.id, States.main, message.chat.id)
    main(message)


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.set_my_commands([
        telebot.types.BotCommand("start", "Запуск бота"),
        telebot.types.BotCommand("help", "Помощь по боту"),
        telebot.types.BotCommand("custom", "Настройка бота"),
        telebot.types.BotCommand("download", "Начать скачивать видео")
    ])
    bot.polling()
