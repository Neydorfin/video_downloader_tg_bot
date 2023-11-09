import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase('tg_video_bot.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        db_table = "Users"

    user_id = pw.IntegerField(primary_key=True)
    chat_id = pw.IntegerField()
    username = pw.TextField(null=True)
    first_name = pw.TextField(null=True)
    last_name = pw.TextField(null=True)


class History(BaseModel):
    user_id = pw.ForeignKeyField(User.user_id, null=True)
    history_id = pw.AutoField()
    created_at = pw.DateField(default=datetime.now())
    link = pw.TextField(null=True)
    video_id = pw.TextField(null=True)
    title = pw.TextField(null=True)
    time = pw.TimeField(null=True)
    platform = pw.TextField(null=True)
    resolution = pw.TextField(null=True)
    thumbnail = pw.TextField(null=True)
    video_views = pw.IntegerField(null=True)
    video_size = pw.IntegerField(null=True)
    _140 = pw.TextField(null=True)
    _242 = pw.TextField(null=True)
    _18 = pw.TextField(null=True)
    _244 = pw.TextField(null=True)
    _22 = pw.TextField(null=True)
    _137 = pw.TextField(null=True)
    _271 = pw.TextField(null=True)
    _313 = pw.TextField(null=True)


class UserConfig(BaseModel):
    class Meta:
        db_table = "User_Config"

    user_id = pw.PrimaryKeyField(User.user_id)
    low = pw.CharField(max_length=10)
    high = pw.CharField(max_length=10)
    info = pw.BooleanField()


if __name__ == '__main__':
    db.create_tables([User, UserConfig, History])
