from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)


def create_custom_forecast_keyboard(*args) -> ReplyKeyboardMarkup:
    """
    Create custom forecast keyboard.
    :param args:
    :type args: list | set
    :return:
    :rtype: ReplyKeyboardMarkup
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for arg in args:
        button = KeyboardButton(arg)
        keyboard.add(button)

    return keyboard


def remove_keyboard() -> ReplyKeyboardRemove:
    """
    Remove keyboard.
    :return:
    :rtype: ReplyKeyboardRemove
    """
    keyboard = ReplyKeyboardRemove()
    return keyboard
