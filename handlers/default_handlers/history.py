from loader import bot
from telebot.types import Message
from database.redis_database import RedisDatabaseInterface
import json


@bot.message_handler(commands=['history'])
def handle_history(message: Message) -> None:
    history = json.loads(RedisDatabaseInterface.get_redis(message.from_user.id, 'history'))
    if len(history) == 1:
        bot.send_message(message.chat.id, history)
    else:
        history_str = '\n'.join(['History:', *history])
        bot.send_message(message.chat.id, history_str)
    RedisDatabaseInterface.add_history(message.from_user.id, message)
