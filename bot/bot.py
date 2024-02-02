import telebot
from telebot.types import Message
from config import BOT_TOKEN, DEFAULT_COMMANDS
from database.database_orm import User
from peewee import IntegrityError
from api.get_weather import GetWeatherInterface
from api.get_loc_from_ip import GetLocationInterface
from utils.weather_parser import WeatherParser
from states.states import MyStates
from database.redis_database import RedisDatabaseInterface
from telebot import custom_filters
import re
import json


bot = telebot.TeleBot(BOT_TOKEN)


def start_bot():
    @bot.message_handler(commands=['start'])
    def handle_start(message: Message) -> None:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name

        try:
            user = User.create(
                user_id=user_id,
                username=username,
                first_name=first_name,
            )
            user.save()
            bot.reply_to(message, "Welcome! I'm bot for weather forecast."
                                  " Type /help for a list of commands and their descriptions.")
        except IntegrityError:
            bot.reply_to(message, "Glad to see you again, {first_name}! Write /help"
                                  " to get a list of commands and their descriptions.".format(first_name=first_name))

    @bot.message_handler(commands=['help'])
    def handle_help(message: Message) -> None:
        commands = ["/{}".format(' - '.join(command)) for command in DEFAULT_COMMANDS]
        bot.send_message(message.chat.id, "\n{}".format('\n'.join(commands)))

    @bot.message_handler(commands=['weather_forecast'])
    def handle_weather_forecast(message: Message) -> None:
        try:
            weather = GetWeatherInterface.get_weather()
            structured_weather = WeatherParser.structured_weather_forecast(weather)
            bot.send_message(message.chat.id, WeatherParser.print_weather_forecast(structured_weather))
            bot.send_message(message.chat.id, "For more information, write a date from"
                                              " the list above to see detailed forecast")

            RedisDatabaseInterface.set_redis('weather', structured_weather)
            RedisDatabaseInterface.set_redis('location', GetLocationInterface.get_location()['city_name'])
            bot.set_state(message.from_user.id, MyStates.forecast, message.chat.id)
        except ValueError as error:
            bot.send_message(message.chat.id, str(error))

    @bot.message_handler(state=MyStates.forecast)
    def handle_forecast(message: Message) -> None:
        forecast_date = message.text
        if re.match(r'\b\d{2}.\d{2}\b', forecast_date):
            try:
                forecast_info = json.loads(RedisDatabaseInterface.get_redis('weather'))[message.text]
                location = RedisDatabaseInterface.get_redis('location').decode('utf-8')
                bot.send_message(message.chat.id, WeatherParser.print_weather_forecast_item((forecast_date,
                                                                                             forecast_info)
                                                                                            , location))
            except KeyError:
                bot.send_message(message.chat.id, "Write a date from the list above to see detailed forecast.\n"
                                                  "If you want to see other weather forecast, try another command")
        else:
            bot.send_message(message.chat.id, "Write a date from the list above to see detailed forecast.\n"
                                              "If you want to see other weather forecast, try another command")

    bot.add_custom_filter(custom_filters.StateFilter(bot))

    bot.polling(none_stop=True)
