from database.common.models import db, User, UserConfig, History
from database.utils.CRUD import CRUDInteface

db.connect()
db.create_tables([User, UserConfig, History])

crud = CRUDInteface()

