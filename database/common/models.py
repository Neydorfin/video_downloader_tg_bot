import peewee as pw
from datetime import datetime

db = pw.SqliteDatabase('../tg_video_bot.db')


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        db_table = "Users"

    user_id = pw.IntegerField(primary_key=True)
    chat_id = pw.IntegerField()
    username = pw.CharField(max_length=150)


class History(BaseModel):
    history_id = pw.AutoField()
    user_id = pw.ForeignKeyField(User, backref='user_id')
    created_at = pw.DateField(default=datetime.now())
    link = pw.TextField()
    video_name = pw.TextField()
    video_views = pw.IntegerField()
    video_size = pw.IntegerField()
    message = pw.TextField()


class UserConfig(BaseModel):
    user_id = pw.ForeignKeyField(User, backref='user_id')
    low = pw.CharField(max_length=10)
    high = pw.CharField(max_length=10)
    info = pw.BooleanField()


if __name__ == '__main__':
    db.create_tables([User, UserConfig, History])
