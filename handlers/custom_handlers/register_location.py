from loader import bot
from telebot.types import Message
from database.redis_database import RedisDatabaseInterface
from states.states import MyStates


@bot.message_handler(content_types=['location'], state=MyStates.set_location)
def handle_location_1(message: Message) -> None:
    if bot.get_state(message.from_user.id, message.chat.id) is not None:
        bot.delete_state(message.from_user.id, message.chat.id)
    RedisDatabaseInterface.set_redis(message.from_user.id, "location", {"latitude": message.location.latitude,
                                                                        "longitude": message.location.longitude})
    bot.set_state(message.from_user.id, MyStates.location, message.chat.id)
    bot.send_message(message.chat.id, "Location saved!")


@bot.message_handler(func=lambda message: not message.text.startswith('/'), regexp=r'\D+',
                     content_types=['text'], state=MyStates.set_location)
def handle_location_2(message: Message) -> None:
    if bot.get_state(message.from_user.id, message.chat.id) is not None:
        bot.delete_state(message.from_user.id, message.chat.id)
    RedisDatabaseInterface.set_redis(message.from_user.id, "location", message.text)
    bot.set_state(message.from_user.id, MyStates.location, message.chat.id)
    bot.send_message(message.chat.id, "Location saved!")
