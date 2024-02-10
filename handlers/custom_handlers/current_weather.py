from loader import bot
from telebot.types import Message
from states.states import MyStates
from api.get_weather import GetWeatherInterface
from utils.weather_parser import WeatherParser
from database.redis_database import RedisDatabaseInterface
import json


@bot.message_handler(commands=['current_weather'], state=[MyStates.location, MyStates.forecast])
def handle_current_weather(message: Message) -> None:
    try:
        current_weather = GetWeatherInterface.get_weather(message.from_user.id, '1h')
        print(current_weather)
        # print(RedisDatabaseInterface.get_redis(message.from_user.id, 'current_weather'))
        structured_current_weather = WeatherParser.structured_current_weather(current_weather)
        print(structured_current_weather)
        bot.send_message(message.chat.id, WeatherParser.print_current_weather(message.from_user.id,
                                                                              structured_current_weather))

    except ValueError as error:
        bot.send_message(message.chat.id, str(error))

