from telebot.apihelper import ApiTelegramException
from loader import bot
from telebot.types import Message, CallbackQuery
from states.states import MyStates
from api.get_weather import GetWeatherInterface
from api.get_timezone import GetTimeZoneInterface
from utils.weather_parser import WeatherParser
from database.redis_database import RedisDatabaseInterface
from keyboards.reply.custom_forecast_keyboard import (
    create_custom_forecast_keyboard,
    remove_keyboard,
)
from keyboards.inline.parameters_keyboard import (
    create_custom_inline_keyboard,
    NEXT,
    PREV,
)
from utils.handler_functions import (
    next_prev_preprocessor,
    next_prev_postprocessor,
)


@bot.message_handler(
    commands=["custom_forecast"], state=[MyStates.location, MyStates.forecast]
)
def handle_custom_forecast(message: Message) -> None:
    """
    Handle /custom_forecast command if the state is set.
    :param message:
    :type message: Message
    :return:
    :rtype: None
    """
    try:
        RedisDatabaseInterface.delete_redis(message.from_user.id, "message_id")
    except Exception as e:
        print(e)
    keyboard = create_custom_forecast_keyboard(
        "Timesteps: 1h", "Timesteps: 1d"
    )
    bot.send_message(
        message.chat.id, "Choose a timestep:", reply_markup=keyboard
    )
    RedisDatabaseInterface.add_history(message.from_user.id, message)
    bot.set_state(message.from_user.id, MyStates.timesteps, message.chat.id)


@bot.message_handler(state="*", commands=["custom_forecast"])
def handle_custom_forecast(message: Message) -> None:
    """
    Handle /custom_forecast command if the state is not set.
    :param message:
    :return:
    """
    RedisDatabaseInterface.add_history(message.from_user.id, message)
    bot.send_message(
        message.chat.id,
        "Your location is not set! Please, use /set_location command.",
    )


@bot.message_handler(
    state=MyStates.timesteps, regexp=r"\bTimesteps: 1h\b|\bTimesteps: 1d\b"
)
def handle_timesteps(message: Message) -> None:
    """
    Handle timesteps message.
    :param message:
    :type message: Message
    :return:
    :rtype: None
    """
    timesteps = message.text[-2:]
    RedisDatabaseInterface.set_redis(
        message.from_user.id, "timesteps", timesteps
    )
    bot.send_message(message.chat.id, "Saved!")
    bot.send_message(
        message.chat.id,
        "Choose a unit:",
        reply_markup=create_custom_forecast_keyboard("Metric", "Imperial"),
    )
    RedisDatabaseInterface.add_history(message.from_user.id, message)
    bot.set_state(message.from_user.id, MyStates.units, message.chat.id)


@bot.message_handler(state=MyStates.units, regexp=r"\bMetric\b|\bImperial\b")
def handle_units(message: Message) -> None:
    """
    Handle units message.
    :param message:
    :type message: Message
    :return:
    :rtype: None
    """
    units = message.text.lower()
    units_message = "metric" if units == "metric" else "imperial"
    RedisDatabaseInterface.set_redis(message.from_user.id, "units", units)
    bot.set_state(message.from_user.id, MyStates.keys, message.chat.id)
    bot.send_message(message.chat.id, "Saved!", reply_markup=remove_keyboard())

    timesteps = RedisDatabaseInterface.get_redis(
        message.from_user.id, "timesteps"
    )
    timesteps_message = "hourly" if timesteps == "1h" else "daily"
    weather = GetWeatherInterface.get_weather(
        message.from_user.id, timesteps, units
    )
    RedisDatabaseInterface.set_redis(message.from_user.id, "weather", weather)
    if timesteps == "1h":
        GetTimeZoneInterface.get_time_zone(message.from_user.id)
    WeatherParser.custom_weather_parser(message.from_user.id, timesteps, units)
    keyboard = create_custom_inline_keyboard("Show forecast")
    bot.send_message(
        message.from_user.id,
        "Press this button to show {timesteps} forecast"
        " in {units} units".format(
            timesteps=timesteps_message, units=units_message
        ),
        reply_markup=keyboard,
    )

    RedisDatabaseInterface.add_history(message.from_user.id, message)


@bot.callback_query_handler(func=lambda call: call.data == "Show forecast")
def handle_next_prev(call: CallbackQuery) -> None:
    """
    Handle next and previous buttons.
    :param call:
    :type call: CallbackQuery
    :return:
    :rtype: None
    """
    bot.edit_message_text(
        "Loading...", call.message.chat.id, call.message.message_id
    )
    message = call.message
    forecast = next_prev_preprocessor(call)
    keyboard, time = next_prev_postprocessor(call, forecast)
    bot.send_message(
        message.chat.id, "Forecast for {}".format(time), reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data == NEXT.callback_data)
def handle_next(call: CallbackQuery) -> None:
    """
    Handle next button.
    :param call:
    :type call: CallbackQuery
    :return:
    :rtype: None
    """
    message = call.message
    forecast = next_prev_preprocessor(call)
    keyboard, time = next_prev_postprocessor(call, forecast, 1)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Forecast for {}".format(time),
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: call.data == PREV.callback_data)
def handle_prev(call: CallbackQuery) -> None:
    """
    Handle previous button.
    :param call:
    :type call: CallbackQuery
    :return:
    :rtype: None
    """
    message = call.message
    forecast = next_prev_preprocessor(call)
    keyboard, time = next_prev_postprocessor(call, forecast, -1)
    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text="Forecast for {}".format(time),
        reply_markup=keyboard,
    )


@bot.callback_query_handler(
    func=lambda call: call.data in WeatherParser.get_timely_callbacks(call)
)
def handle_timely_forecast(call) -> None:
    """
    Handle button for forecast of certain timestep.
    :param call:
    :type call: CallbackQuery
    :return:
    :rtype: None
    """
    current_time = RedisDatabaseInterface.get_redis(
        call.from_user.id, "current_time"
    )
    forecast = next_prev_preprocessor(call)
    key = list(forecast.keys())[current_time]
    value = forecast[key][call.data]
    message = RedisDatabaseInterface.get_redis(call.from_user.id, "message_id")
    if message is None:
        new_message = bot.send_message(
            chat_id=call.message.chat.id,
            text="Forecast for {}: {}".format(call.data, value),
        )
        RedisDatabaseInterface.set_redis(
            call.from_user.id, "message_id", new_message.message_id
        )
    else:
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                text="Forecast for {}: {}".format(call.data, value),
                message_id=message,
            )
        except ApiTelegramException:
            pass
