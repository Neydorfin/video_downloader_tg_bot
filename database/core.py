from database.common.models import db, User, UserConfig, History
from database.utils.CRUD import CRUDInterface

db.connect()
db.create_tables([User, UserConfig, History])


class Models:
    User = User
    UserConfig = UserConfig
    History = History


class DataBase:
    db = db

    crud = CRUDInterface()
    models = Models()
    write = crud.create()
    update = crud.update()
    read = crud.retrieve()


if __name__ == '__main__':
    DataBase()

