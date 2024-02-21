from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS
from database.redis_database import RedisDatabaseInterface


@bot.message_handler(commands=["help"])
def handle_help(message: Message) -> None:
    """
    Handle /help command.
    :param message:
    :type message: Message
    :return:
    :rtype: None
    """
    if bot.get_state(message.from_user.id, message.chat.id) is not None:
        bot.delete_state(message.from_user.id, message.chat.id)
    commands = [
        "/{}".format(" - ".join(command)) for command in DEFAULT_COMMANDS
    ]
    bot.send_message(message.chat.id, "\n{}".format("\n".join(commands)))

    RedisDatabaseInterface.add_history(message.from_user.id, message)
