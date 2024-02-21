from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    """States for commands handling."""

    forecast = State()
    location = State()
    set_location = State()
    timesteps = State()
    units = State()
    keys = State()
