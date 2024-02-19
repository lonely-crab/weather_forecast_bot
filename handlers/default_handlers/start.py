from telebot.types import Message
from loader import bot
from database.database_orm import User
from peewee import IntegrityError
from database.redis_database import RedisDatabaseInterface


@bot.message_handler(commands=["start"])
def handle_start(message: Message) -> None:
    if bot.get_state(message.from_user.id, message.chat.id) is not None:
        bot.delete_state(message.from_user.id, message.chat.id)
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    RedisDatabaseInterface.set_user(message.from_user.id)

    try:
        user = User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
        )
        user.save()
        bot.reply_to(
            message,
            "Welcome! I'm bot for weather forecast."
            " Type /help for a list of commands and their descriptions.",
        )
    except IntegrityError:
        bot.reply_to(
            message,
            "Glad to see you again, {first_name}! Write /help"
            " to get a list of commands and their descriptions.".format(
                first_name=first_name
            ),
        )
    RedisDatabaseInterface.add_history(message.from_user.id, message)
