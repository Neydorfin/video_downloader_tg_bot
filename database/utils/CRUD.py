from typing import Dict, TypeVar
from peewee import ModelSelect
from database.common.models import db

T = TypeVar("T")


def _store_date(database: db, model: T, data: Dict) -> None:
    with database.atomic():
        model.insert(**data).execute()


def _retrieve_all_data(database: db, model: T, user_id: int) -> ModelSelect:
    print("CRUD:", user_id)
    with database.atomic():
        # response = model.select().where(model.user_id == user_id)
        try:
            response = model.get_by_id(user_id)
        except:
            response = None
    return response


def _update_data(database: db, model: T, data: Dict, user_id: int) -> None:
    with database.atomic():
        model.update(**data).where(model.user_id == user_id).execute()


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
    _store_date()
    _retrieve_all_data()
    CRUDInterface()
