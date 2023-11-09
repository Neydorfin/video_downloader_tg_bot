from typing import Dict, TypeVar
from peewee import ModelSelect
from database.common.models import db, History, User, UserConfig

T = TypeVar("T")


def _store_date(database: db, model: T, data: Dict) -> None:
    with database.atomic():
        model.insert(**data).execute()


def _retrieve_all_data(database: db, model: T, user_id: int) -> ModelSelect:
    with database.atomic():
        res = []
        if model is not History:
            response = model.get_or_none(user_id)
        else:
            for row in model.select().order_by(History.history_id.desc()).where(user_id == user_id).execute():
                res.append(row)
            response = res[0]
    return response


def _update_data(database: db, model: T, data: Dict, user_id: int) -> None:
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
    _store_date()
    _retrieve_all_data()
    CRUDInterface()
