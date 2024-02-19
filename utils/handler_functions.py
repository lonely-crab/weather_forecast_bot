from telebot.types import CallbackQuery
from database.redis_database import RedisDatabaseInterface
from keyboards.inline.parameters_keyboard import (
    create_custom_inline_keyboard,
    NEXT,
    PREV,
)
from telebot.types import InlineKeyboardMarkup


def next_prev_preprocessor(call: CallbackQuery) -> dict[str, dict]:
    timesteps = RedisDatabaseInterface.get_redis(
        call.from_user.id, "timesteps"
    )
    timesteps_query = "hourly" if timesteps == "1h" else "daily"
    forecast = RedisDatabaseInterface.get_redis(
        call.from_user.id, timesteps_query
    )
    return forecast


def next_prev_postprocessor(
    call: CallbackQuery, forecast: dict, step: int = 0
) -> tuple[InlineKeyboardMarkup, str]:
    times = list(forecast.keys())
    current_time = RedisDatabaseInterface.get_redis(
        call.from_user.id, "current_time"
    )
    try:
        if step == 0:
            time = times[0]
        else:
            time = times[current_time + step]
    except IndexError:
        pass
    current_time = times.index(time)
    RedisDatabaseInterface.set_redis(
        call.from_user.id, "current_time", current_time
    )
    keyboard = create_custom_inline_keyboard(*forecast[time])
    if current_time != len(times) - 1:
        keyboard.add(NEXT)
    if current_time != 0:
        keyboard.add(PREV)
    return keyboard, time
