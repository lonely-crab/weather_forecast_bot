from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def create_custom_forecast_keyboard(*args) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for arg in args:
        button = KeyboardButton(arg)
        keyboard.add(button)

    return keyboard


def remove_keyboard() -> ReplyKeyboardRemove:
    keyboard = ReplyKeyboardRemove()
    return keyboard

