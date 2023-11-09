import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()


class BotSettings:
    BOT_TOKEN = os.getenv('BOT_TOKEN', None)


if BotSettings.BOT_TOKEN is None:
    exit('BOT_TOKEN отсутствует в переменных окружения')


COUB_HOST_API = "https://coub.com/api/v2/coubs"
