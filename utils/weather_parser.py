from datetime import datetime
from datetime import timedelta
from database.redis_database import RedisDatabaseInterface
from .conditions import Conditions

_weather_emojis = {
    "temperatureMax": "\U0001F321",  # 🌡️
    "temperatureMin": "\u2744\uFE0F",  # ❄️
    "cloudCoverAvg": "\u2601\uFE0F",  # ☁️
    "windSpeedAvg": "\U0001F32C",  # 🌬️
    "windGustMax": "\U0001F4A8",  # 💨
    "humidityAvg": "\U0001F4A7",  # 💧
    "pressureSurfaceLevelAvg": "\U0001F4CA",  # 📊
    "precipitationProbabilityMax": "\U0001F327",  # 🌧️
}


def _structured_weather_forecast(weather_forecast: dict) -> dict:
    weather_dict = {}
    keys = [
        "temperatureMax",
        "temperatureMin",
        "cloudCoverAvg",
        "windSpeedAvg",
        "windGustMax",
        "humidityAvg",
        "pressureSurfaceLevelAvg",
        "precipitationProbabilityMax",
    ]
    for day in weather_forecast["timelines"]["daily"]:
        formatted_date = datetime.fromisoformat(day["time"]).strftime("%d.%m")
        weather_dict[formatted_date] = {
            key: day["values"][key] for key in keys
        }

    return weather_dict


def _structured_current_weather(user_id, current_weather: dict) -> dict:
    keys = [
        "temperature",
        "cloudCover",
        "windSpeed",
        "rainAccumulation",
        "sleetAccumulation",
        "snowAccumulation",
        "precipitationProbability",
    ]
    weather_dict = {}
    timedel = RedisDatabaseInterface.get_redis(user_id, "timezone")
    for hour in current_weather["timelines"]["hourly"]:
        if timedel.startswith("-"):
            timed = timedel[1:3]
            time = datetime.fromisoformat(hour["time"]) - timedelta(
                hours=int(timed)
            )
        else:
            timed = timedel[1:3]
            time = datetime.fromisoformat(hour["time"]) + timedelta(
                hours=int(timed)
            )
        time = time.strftime("%H:%M")
        if time in weather_dict:
            continue
        weather = {key: hour["values"][key] for key in keys}
        print(weather)
        weather_dict[time] = weather
    return weather_dict


def _print_weather_forecast_item(
    user_id, weather_forecast_item: tuple, location: str | None = None
) -> str:
    if location is None:
        location = RedisDatabaseInterface.get_redis(user_id, "city")
    if location is None:
        location = RedisDatabaseInterface.get_redis(user_id, "location")
    if location is None:
        location = ""

    weather_summary = (
        "Weather forecast for {} at {}:\n"
        "    {emoji1}Maximum Temperature: {:.0f}°C\n"
        "    {emoji2}Minimum Temperature: {:.0f}°C\n"
        "    {emoji3}Average Cloud Cover: {:.2f}%\n"
        "    {emoji4}Average Wind Speed: {:.2f} m/s\n"
        "    {emoji5}Maximum Wind Gust: {:.2f} m/s\n"
        "    {emoji6}Average Humidity: {:.2f}%\n"
        "    {emoji7}Average Surface-Level Pressure: {:.2f} hPa\n"
        "    {emoji8}Maximum Precipitation Probability: {:.0f}%"
    )

    formatted_summary = weather_summary.format(
        weather_forecast_item[0],
        location,
        round(weather_forecast_item[1]["temperatureMax"]),
        round(weather_forecast_item[1]["temperatureMin"]),
        weather_forecast_item[1]["cloudCoverAvg"],
        round(weather_forecast_item[1]["windSpeedAvg"]),
        round(weather_forecast_item[1]["windGustMax"]),
        weather_forecast_item[1]["humidityAvg"],
        weather_forecast_item[1]["pressureSurfaceLevelAvg"],
        weather_forecast_item[1]["precipitationProbabilityMax"],
        emoji1=_weather_emojis["temperatureMax"],
        emoji2=_weather_emojis["temperatureMin"],
        emoji3=_weather_emojis["cloudCoverAvg"],
        emoji4=_weather_emojis["windSpeedAvg"],
        emoji5=_weather_emojis["windGustMax"],
        emoji6=_weather_emojis["humidityAvg"],
        emoji7=_weather_emojis["pressureSurfaceLevelAvg"],
        emoji8=_weather_emojis["precipitationProbabilityMax"],
    )

    return formatted_summary


def _print_weather_forecast(user_id, weather_forecast: dict) -> str:
    weather_list = list(weather_forecast.items())
    weather_summary = [_print_weather_forecast_item(user_id, weather_list[0])]
    short_summary = (
        "\nWeather forecast for {}:\n    {emoji1}Maximum Temperature: {:.0f}°C\n"
        "    {emoji2}Minimum Temperature: {:.0f}°C"
    )

    weather_summary.extend(
        [
            short_summary.format(
                weather_forecast_item[0],
                round(weather_forecast_item[1]["temperatureMax"]),
                round(weather_forecast_item[1]["temperatureMin"]),
                emoji1=_weather_emojis["temperatureMax"],
                emoji2=_weather_emojis["temperatureMin"],
            )
            for weather_forecast_item in weather_list[1:]
        ]
    )

    return "\n".join(weather_summary)


def _print_current_weather(user_id, current_weather: dict) -> str:
    keys = [
        "temperature",
        "cloudCover",
        "windSpeed",
        "rainAccumulation",
        "sleetAccumulation",
        "snowAccumulation",
        "precipitationProbability",
    ]

    location = RedisDatabaseInterface.get_redis(user_id, "city")
    if location is None:
        location = RedisDatabaseInterface.get_redis(user_id, "location")
    if location is None:
        location = ""

    weather_item = (
        "{time} {cloudCover} {temperature:.0f}°C -- {windEmoji}{windSpeed:.2f} m/s"
        " -- {accumulation}{precipitation:.0f}%\n"
    )
    weather_summary = "Current weather at {}:\n".format(location)

    for time in current_weather:
        emojis = Conditions.choose_emoji(current_weather[time])
        accumulation = [key for key in emojis if key.endswith("Accumulation")][
            0
        ]
        formatted_weather_item = weather_item.format(
            time=time,
            temperature=current_weather[time]["temperature"],
            cloudCover=emojis["cloudCover"],
            windEmoji=emojis["windSpeed"],
            windSpeed=current_weather[time]["windSpeed"],
            accumulation=emojis[accumulation],
            precipitation=current_weather[time]["precipitationProbability"],
        )
        weather_summary = "".join([weather_summary, formatted_weather_item])
    return weather_summary


def _hourly_custom_forecast(weather: dict, timedel):
    weather_dict = {}
    banned_keys = {
        "iceAccumulationLwe",
        "rainAccumulationLwe",
        "snowAccumulationLwe",
        "sleetAccumulationLwe",
        "temperatureApparent",
        "weatherCode",
    }
    for hour in weather["timelines"]["hourly"]:
        if timedel.startswith("-"):
            timed = timedel[1:3]
            time = datetime.fromisoformat(hour["time"]) - timedelta(
                hours=int(timed)
            )
        else:
            timed = timedel[1:3]
            time = datetime.fromisoformat(hour["time"]) + timedelta(
                hours=int(timed)
            )
        time = time.strftime("%H:%M")
        if len(weather_dict) == 24:
            break
        if time in weather_dict:
            continue
        new_values = {
            key: val
            for key, val in hour["values"].items()
            if val is not None and key not in banned_keys
        }
        weather_dict[time] = new_values
    return weather_dict


def _daily_custom_forecast(weather: dict):
    weather_dict = {}
    allowed_keys = {
        "cloudBaseAvg",
        "cloudCeilingAvg",
        "cloudCoverAvg",
        "dewPointAvg",
        "evapotranspirationAvg",
        "freezingRainIntensityAvg",
        "humidityAvg",
        "iceAccumulationAvg",
        "moonriseTime",
        "precipitationProbabilityAvg",
        "uvHealthConcernAvg",
        "pressureSurfaceLevelAvg",
        "rainAccumulationAvg",
        "rainIntensityAvg",
        "sleetAccumulationAvg",
        "sleetIntensityAvg",
        "snowAccumulationAvg",
        "snowIntensityAvg",
        "sunriseTime",
        "sunsetTime",
        "temperatureAvg",
        "temperatureMax",
        "temperatureMin",
        "uvIndexAvg",
        "visibilityAvg",
        "windDirectionAvg",
        "windSpeedAvg",
        "windGustMax",
    }
    for day in weather["timelines"]["daily"]:
        formatted_date = datetime.fromisoformat(day["time"]).strftime("%d.%m")
        new_values = {
            key: value
            for key, value in day["values"].items()
            if value is not None and key in allowed_keys
        }
        weather_dict[formatted_date] = new_values
    return weather_dict


def _custom_weather_parser(user_id, timesteps: str, units: str):
    timedel = RedisDatabaseInterface.get_redis(user_id, "timezone")
    weather = RedisDatabaseInterface.get_redis(user_id, "weather")
    if timesteps == "1h":
        RedisDatabaseInterface.set_redis(
            user_id, "hourly", _hourly_custom_forecast(weather, timedel)
        )
    else:
        RedisDatabaseInterface.set_redis(
            user_id, "daily", _daily_custom_forecast(weather)
        )


def _get_timely_callbacks(call) -> list:
    timesteps = RedisDatabaseInterface.get_redis(
        call.from_user.id, "timesteps"
    )
    timesteps_query = "hourly" if timesteps == "1h" else "daily"
    forecast = RedisDatabaseInterface.get_redis(
        call.from_user.id, timesteps_query
    )
    current_time = RedisDatabaseInterface.get_redis(
        call.from_user.id, "current_time"
    )
    times = list(forecast.keys())
    time = times[current_time]
    values = list(forecast[time].keys())
    return values


class WeatherParser:
    @classmethod
    def structured_weather_forecast(cls, weather_forecast):
        return _structured_weather_forecast(weather_forecast)

    @classmethod
    def print_weather_forecast(cls, user_id, weather_forecast):
        return _print_weather_forecast(user_id, weather_forecast)

    @classmethod
    def print_weather_forecast_item(
        cls, user_id, weather_forecast_item, location=None
    ):
        return _print_weather_forecast_item(
            user_id, weather_forecast_item, location
        )

    @classmethod
    def structured_current_weather(cls, user_id, current_weather):
        return _structured_current_weather(user_id, current_weather)

    @classmethod
    def print_current_weather(cls, user_id, current_weather):
        return _print_current_weather(user_id, current_weather)

    @classmethod
    def custom_weather_parser(cls, user_id, timesteps, units):
        return _custom_weather_parser(user_id, timesteps, units)

    @classmethod
    def get_timely_callbacks(cls, call):
        return _get_timely_callbacks(call)


if __name__ == "__main__":
    pass
