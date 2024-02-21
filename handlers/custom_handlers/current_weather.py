from loader import bot
from telebot.types import Message
from states.states import MyStates
from api.get_weather import GetWeatherInterface
from api.get_timezone import GetTimeZoneInterface
from utils.weather_parser import WeatherParser
from database.redis_database import RedisDatabaseInterface


@bot.message_handler(
    commands=["current_weather"], state=[MyStates.location, MyStates.forecast]
)
def handle_current_weather(message: Message) -> None:
    """
    Handle /current_weather command
    :param message:
    :type message: Message
    :return:
    :rtype: None
    """
    try:
        current_weather = GetWeatherInterface.get_weather(
            message.from_user.id, "1h"
        )
        GetTimeZoneInterface.get_time_zone(message.from_user.id)
        structured_current_weather = WeatherParser.structured_current_weather(
            message.from_user.id, current_weather
        )
        print(structured_current_weather)
        bot.send_message(
            message.chat.id,
            WeatherParser.print_current_weather(
                message.from_user.id, structured_current_weather
            ),
        )
        RedisDatabaseInterface.add_history(message.from_user.id, message)

    except ValueError as error:
        bot.send_message(message.chat.id, str(error))
