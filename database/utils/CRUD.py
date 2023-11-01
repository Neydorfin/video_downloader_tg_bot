from typing import Dict, List, TypeVar, Tuple
from peewee import ModelSelect
from database.common.models import db, BaseModel

T = TypeVar("T")


def _store_date(db: db, model: T, data: Dict) -> None:
    with db.atomic():
        model.insert(**data).execute()


def _retrieve_all_data(db: db, model: T, user_id: int) -> ModelSelect:
    with db.atomic():
        response = model.select().where(user_id == user_id)
    return response


def _update_data(db: db, model: T, data: Dict, user_id: int) -> None:
    with db.atomic():
        response = model.update(**data).where(model.user_id == user_id).execute()


class CRUDInteface():
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
    CRUDInteface()
