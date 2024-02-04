from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS
from states.states import MyStates

@bot.message_handler(commands=['help'])
def handle_help(message: Message) -> None:
    if bot.get_state(message.from_user.id, message.chat.id) is not None:
        bot.delete_state(message.from_user.id, message.chat.id)
    commands = ["/{}".format(' - '.join(command)) for command in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, "\n{}".format('\n'.join(commands)))

