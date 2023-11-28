from typing import Dict, TypeVar
from peewee import ModelSelect
from database.common.models import db, History, User, UserConfig
from utils.logging import logger

T = TypeVar("T")


@logger
def _store_date(database: db, model: T, data: Dict) -> None:
    """
        Сохраняет данные в базе данных.

        Args:
            database (db): Объект базы данных Peewee.
            model (T): Модель Peewee для сохранения данных.
            data (Dict): Словарь с данными для сохранения.

        Returns:
            None
        """
    with database.atomic():
        model.insert(**data).execute()


@logger
def _retrieve_all_data(database: db, model: T, user_id: int, limit: int = 1) -> ModelSelect:
    """
        Получает все данные из базы данных.

        Args:
            database (db): Объект базы данных Peewee.
            model (T): Модель Peewee для извлечения данных.
            user_id (int): Идентификатор пользователя.

        Returns:
            ModelSelect: Результат запроса к базе данных.
    """
    with database.atomic():
        res = []
        if model is not History:
            response = model.get_or_none(user_id)
        else:
            for row in model.select().order_by(History.history_id.desc()).where(user_id == user_id).execute():
                res.append(row)
            if limit == 1:
                response = res[0]
            else:
                response = res[:int(limit) + 1]
    return response


@logger
def _update_data(database: db, model: T, data: Dict, user_id: int) -> None:
    """
        Обновляет данные в базе данных.

        Args:
            database (db): Объект базы данных Peewee.
            model (T): Модель Peewee для обновления данных.
            data (Dict): Словарь с данными для обновления.
            user_id (int): Идентификатор пользователя.

        Returns:
            None
        """
    with database.atomic():
        if model is not History:
            model.update(**data).where(model.user_id == user_id).execute()
        else:
            model.update(**data).where(model.history_id == user_id).execute()


class CRUDInterface:
    @staticmethod
    def create():
        return _store_date

    @staticmethod
    def retrieve():
        return _retrieve_all_data

    @staticmethod
    def update():
        return _update_data


if __name__ == "__main__":
    CRUDInterface()
