from telebot.types import BotCommand
from telebot import TeleBot
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot: TeleBot) -> None:
    """
    Set default commands.
    :param bot:
    :type bot: TeleBot
    :return:
    :rtype: None
    """
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])
