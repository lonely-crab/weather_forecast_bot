from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    forecast = State()
