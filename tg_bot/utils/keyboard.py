from telebot import types


class Buttons:
    # platform selector
    platform_markup = types.ReplyKeyboardMarkup(row_width=3)
    _YouTube_button = types.KeyboardButton("Youtube")
    _Vk_button = types.KeyboardButton("Vk")
    _Coub_button = types.KeyboardButton("Coub")
    platform_markup.add(_YouTube_button, _Vk_button, _Coub_button)

    # low resolution selector
    low_markup = types.ReplyKeyboardMarkup(row_width=3)
    _p_240_button = types.KeyboardButton("240p")
    _p_360_button = types.KeyboardButton("360p")
    _p_480_button = types.KeyboardButton("480p")
    low_markup.add(_p_480_button, _p_360_button, _p_240_button)

    # high resolution selector
    high_markup = types.ReplyKeyboardMarkup(row_width=3)
    _p_1080_button = types.KeyboardButton("1080p")
    _p_1440_button = types.KeyboardButton("1440p")
    _p_2160_button = types.KeyboardButton("2160p")
    high_markup.add(_p_2160_button, _p_1440_button, _p_1080_button)

    # switcher
    switch_markup = types.ReplyKeyboardMarkup(row_width=2)
    _on_button = types.KeyboardButton("ВКЛ")
    _off_button = types.KeyboardButton("ВЫКЛ")
    switch_markup.add(_on_button, _off_button)

    # answer
    answer_markup = types.ReplyKeyboardMarkup(row_width=2)
    _yes_button = types.KeyboardButton("Да")
    _no_button = types.KeyboardButton("Нет")
    answer_markup.add(_yes_button, _no_button)

    # remove keyboard
    remove = types.ReplyKeyboardRemove()
