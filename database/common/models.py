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
    time_sec = pw.IntegerField(null=True)
    time = pw.TimeField(null=True)
    platform = pw.TextField(null=True)
    resolution = pw.TextField(null=True)
    thumbnail = pw.TextField(null=True)
    video_views = pw.IntegerField(null=True)
    audio = pw.TextField(null=True)  # audio
    _240 = pw.TextField(null=True)  # 240p
    file_size_240 = pw.FloatField(null=True)  # 240p file_size
    _360 = pw.TextField(null=True)  # 360p
    file_size_360 = pw.FloatField(null=True)  # 360p file_size
    _480 = pw.TextField(null=True)  # 480p
    file_size_480 = pw.FloatField(null=True)  # 480p file_size
    _720 = pw.TextField(null=True)  # 720p
    file_size_720 = pw.FloatField(null=True)  # 720p file_size
    _1080 = pw.TextField(null=True)  # 1080p
    file_size_1080 = pw.FloatField(null=True)  # 1080p file_size
    _1440 = pw.TextField(null=True)  # 1440p
    file_size_1440 = pw.FloatField(null=True)  # 1440p file_size
    _2160 = pw.TextField(null=True)  # 2160p
    file_size_2160 = pw.FloatField(null=True)  # 2160p file_size


class UserConfig(BaseModel):
    class Meta:
        db_table = "User_Config"

    user_id = pw.PrimaryKeyField(User.user_id)
    low = pw.CharField(max_length=10)
    high = pw.CharField(max_length=10)
    info = pw.BooleanField()


if __name__ == '__main__':
    db.create_tables([User, UserConfig, History])
