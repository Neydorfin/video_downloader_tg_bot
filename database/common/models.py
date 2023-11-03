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
    username = pw.CharField(max_length=150)


class History(BaseModel):
    user_id = pw.PrimaryKeyField(User.user_id)
    history_id = pw.IntegerField()
    created_at = pw.DateField(default=datetime.now())
    link = pw.TextField()
    video_name = pw.TextField()
    video_views = pw.IntegerField()
    video_size = pw.IntegerField()
    message = pw.TextField()


class UserConfig(BaseModel):
    class Meta:
        db_table = "User_Config"
    user_id = pw.PrimaryKeyField(User.user_id)
    low = pw.CharField(max_length=10)
    high = pw.CharField(max_length=10)
    info = pw.BooleanField()


if __name__ == '__main__':
    db.create_tables([User, UserConfig, History])
