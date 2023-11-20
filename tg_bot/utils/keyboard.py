from telebot import types


class Buttons:
    # platform selector
    platform_markup = types.ReplyKeyboardMarkup(row_width=1)
    _YouTube_button = types.KeyboardButton("YouTube")
    _Vk_button = types.KeyboardButton("Vk")
    _Coub_button = types.KeyboardButton("Coub")
    platform_markup.add(_YouTube_button, _Vk_button, _Coub_button)

    # low resolution selector
    low_markup = types.ReplyKeyboardMarkup(row_width=1)
    _p_240_button = types.KeyboardButton("240p")
    _p_360_button = types.KeyboardButton("360p")
    _p_480_button = types.KeyboardButton("480p")
    low_markup.add(_p_240_button, _p_360_button, _p_480_button)

    # high resolution selector
    high_markup = types.ReplyKeyboardMarkup(row_width=1)
    _p_1080_button = types.KeyboardButton("1080p")
    _p_1440_button = types.KeyboardButton("1440p")
    _p_2160_button = types.KeyboardButton("2160p")
    high_markup.add(_p_1080_button, _p_1440_button, _p_2160_button)

    # switcher
    switch_markup = types.ReplyKeyboardMarkup(row_width=1)
    _on_button = types.KeyboardButton("ВКЛ")
    _off_button = types.KeyboardButton("ВЫКЛ")
    switch_markup.add(_on_button, _off_button)

    # answer
    answer_markup = types.ReplyKeyboardMarkup(row_width=1)
    _yes_button = types.KeyboardButton("Да")
    _no_button = types.KeyboardButton("Нет")
    answer_markup.add(_yes_button, _no_button)

    # to main
    cancel_markup = types.InlineKeyboardMarkup(row_width=1)
    _cancel_button = types.InlineKeyboardButton("Cancel", callback_data="cancel")
    cancel_markup.add(_cancel_button)

    # remove keyboard
    remove = types.ReplyKeyboardRemove()
