from telebot.types import Message
from loader import bot
from api.get_weather import GetWeatherInterface
from utils.weather_parser import WeatherParser
from states.states import MyStates
from database.redis_database import RedisDatabaseInterface
import re
import json


@bot.message_handler(commands=['weather_forecast'], state=MyStates.location)
def handle_weather_forecast(message: Message) -> None:
    if bot.get_state(message.from_user.id, message.chat.id) is not None:
        bot.delete_state(message.from_user.id, message.chat.id)

    try:
        weather = GetWeatherInterface.get_weather(message.from_user.id)
        structured_weather = WeatherParser.structured_weather_forecast(weather)
        bot.send_message(message.chat.id, WeatherParser.print_weather_forecast(message.from_user.id, structured_weather))
        bot.send_message(message.chat.id, "For more information, write a date from"
                                          " the list above to see detailed forecast")

        RedisDatabaseInterface.set_redis(message.from_user.id, 'weather', structured_weather)
        bot.set_state(message.from_user.id, MyStates.forecast, message.chat.id)
    except ValueError as error:
        bot.send_message(message.chat.id, str(error))


@bot.message_handler(state=MyStates.forecast)
def handle_forecast(message: Message) -> None:
    forecast_date = message.text
    if re.match(r'\b\d{2}.\d{2}\b', forecast_date):
        try:
            forecast_info = RedisDatabaseInterface.get_redis(message.from_user.id, 'weather')[message.text]
            location = RedisDatabaseInterface.get_redis(message.from_user.id, 'city')
            bot.send_message(message.chat.id,
                             WeatherParser.print_weather_forecast_item(message.from_user.id,
                                                    (forecast_date, forecast_info), location))
        except KeyError:
            bot.send_message(message.chat.id, "Write a date from the list above to see detailed forecast.\n"
                                              "If you want to see other weather forecast, try another command")
    else:
        bot.send_message(message.chat.id, "Write a date from the list above to see detailed forecast.\n"
                                          "If you want to see other weather forecast, try another command")
