import telebot
from telebot.types import Message
from config import BOT_TOKEN, DEFAULT_COMMANDS
from database.database_orm import User, db
from peewee import IntegrityError


bot = telebot.TeleBot(BOT_TOKEN)


def start_bot():
    @bot.message_handler(commands=['start'])
    def handle_start(message: Message) -> None:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        try:
            user = User.create(
                user_id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
            )
            user.save()
            bot.reply_to(message, "Добро пожаловать! Напишите /help для получения списка команд и их описания.")
        except IntegrityError:
            bot.reply_to(message, "Рад вас снова видеть, {first_name}! Напишите /help"
                                  " для получения списка команд и их описания.".format(first_name=first_name))

    @bot.message_handler(commands=['help'])
    def handle_help(message: Message) -> None:
        commands = ["/{}".format(' - '.join(command)) for command in DEFAULT_COMMANDS]
        bot.send_message(message.chat.id, "\n{}".format('\n'.join(commands)))

    bot.polling(none_stop=True)
