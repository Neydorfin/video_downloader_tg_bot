from database.common.models import db, User, UserConfig, History
from database.utils.CRUD import CRUDInterface

db.connect()
db.create_tables([User, UserConfig, History])

crud = CRUDInterface()

