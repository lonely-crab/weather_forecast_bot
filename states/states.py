import telebot
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States
from config import BOT_TOKEN

# States storage
from telebot.storage import StateMemoryStorage

# Now, you can pass storage to bot.
state_storage = StateMemoryStorage() # you can init here another storage

bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage)


# States group.
class MyStates(StatesGroup):
    # Just name variables differently
    forecast = State() # creating instances of State class is enough from now


