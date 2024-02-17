from loader import bot
from states.states import MyStates
from telebot.types import Message
from database.redis_database import RedisDatabaseInterface
import json
from datetime import datetime


@bot.message_handler(commands=['history'])
def handle_history(message: Message) -> None:
    bot.send_message(message.chat.id, message.date)
    bot.send_message(message.chat.id, datetime.fromtimestamp(message.date))
    bot.send_message(message.chat.id, 'History')
    history = RedisDatabaseInterface.get_redis(message.from_user.id, 'history')
    if history is None:
        bot.send_message(message.chat.id, 'No history')
    else:
        bot.send_message(message.chat.id, json.dumps(history, indent=4))