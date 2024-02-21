from loader import bot
from telebot.types import Message
from states.states import MyStates
from database.redis_database import RedisDatabaseInterface


@bot.message_handler(commands=["set_location"])
def handle_set_location(message: Message) -> None:
    """
    Handle /set_location command.
    :param message:
    :type message: Message
    :return:
    :rtype: None
    """
    if bot.get_state(message.from_user.id, message.chat.id) is not None:
        bot.delete_state(message.from_user.id, message.chat.id)

    bot.send_message(
        message.chat.id, "Send your location using instructions below:"
    )

    media = ["images/im1.jpeg", "images/im2.jpeg", "images/im3.jpeg"]

    for image in media:
        with open(image, "rb") as photo:
            bot.send_photo(message.chat.id, photo)

    bot.send_message(
        message.chat.id,
        "If you either can't or don't want to share your exact location,"
        " write: country\ncity.",
    )
    bot.send_message(message.chat.id, "For example:\nRussia\nSaint Petersburg")

    bot.set_state(message.from_user.id, MyStates.set_location, message.chat.id)

    RedisDatabaseInterface.add_history(message.from_user.id, message)
