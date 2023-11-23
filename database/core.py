from database.common.models import db, User, UserConfig, History
from database.utils.CRUD import CRUDInterface

# Подключение к базе данных и создание таблиц при необходимости
db.connect()
db.create_tables([User, UserConfig, History])


# Класс Models, который предоставляет доступ к моделям базы данных
class Models:
    User = User
    UserConfig = UserConfig
    History = History


# Класс DataBase, который предоставляет интерфейс для работы с базой данных
class DataBase:
    db = db  # Экземпляр базы данных Peewee

    crud = CRUDInterface()  # Интерфейс CRUD для выполнения операций CRUD
    models = Models()  # Экземпляр класса Models для доступа к моделям базы данных
    write = crud.create()  # Функция создания записи в базе данных
    update = crud.update()  # Функция обновления записи в базе данных
    read = crud.retrieve()  # Функция извлечения данных из базы данных


if __name__ == '__main__':
    DataBase()  # Создание экземпляра класса DataBase при запуске файла
