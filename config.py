import os
from dotenv import load_dotenv, find_dotenv

# Поиск и загрузка переменных окружения из файла .env
if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()


class BotSettings:
    # Получение токена бота из переменных окружения
    BOT_TOKEN = os.getenv('BOT_TOKEN', None)


# Проверка наличия токена бота в переменных окружения
if BotSettings.BOT_TOKEN is None:
    exit('BOT_TOKEN отсутствует в переменных окружения')

# Установка адреса API для Coub
COUB_HOST_API = "https://coub.com/api/v2/coubs"
