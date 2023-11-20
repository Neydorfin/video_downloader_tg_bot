from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    main = State()
    custom = State()
    custom_low = State()
    custom_high = State()
    custom_info = State()
    platform_select = State()
    video_select = State()
    resolution_select = State()
    about_video = State()
    download = State()
    video_maker = State()
    send_video = State()
