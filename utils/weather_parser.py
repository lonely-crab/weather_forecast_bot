import json
from datetime import datetime
from datetime import timezone
from api.get_loc_from_coord import GetLocationInterface


_weather_emojis = {
        "temperatureMax": "\U0001F321",  # 🌡️
        "temperatureMin": "\u2744\uFE0F",  # ❄️
        "cloudCoverAvg": "\u2601\uFE0F",  # ☁️
        "windSpeedAvg": "\U0001F32C",  # 🌬️
        "windGustMax": "\U0001F4A8",  # 💨
        "humidityAvg": "\U0001F4A7",  # 💧
        "pressureSurfaceLevelAvg": "\U0001F4CA",  # 📊
        "precipitationProbabilityMax": "\U0001F327"  # 🌧️
    }


def _structured_weather_forecast(weather_forecast: dict) -> dict:
    weather_dict = {}
    keys = ['temperatureMax', 'temperatureMin', 'cloudCoverAvg', 'windSpeedAvg',
            'windGustMax', 'humidityAvg', 'pressureSurfaceLevelAvg', 'precipitationProbabilityMax']
    for day in weather_forecast['timelines']['daily']:
        formatted_date = datetime.fromisoformat(day['time']).strftime("%d.%m")
        weather_dict[formatted_date] = {key: day['values'][key] for key in keys}

    return weather_dict


def _print_weather_forecast_item(weather_forecast_item: tuple, location: str | None = None) -> str:
    try:
        if location is None:
            location = GetLocationInterface.get_location()['city']
    except KeyError:
        location = ''

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
        emoji8=_weather_emojis["precipitationProbabilityMax"]
    )

    return formatted_summary


def _print_weather_forecast(weather_forecast: dict) -> str:
    weather_list = list(weather_forecast.items())
    weather_summary = [_print_weather_forecast_item(weather_list[0])]
    short_summary = ("\nWeather forecast for {}:\n    {emoji1}Maximum Temperature: {:.0f}°C\n"
                     "    {emoji2}Minimum Temperature: {:.0f}°C")

    weather_summary.extend([short_summary.format(weather_forecast_item[0],
                                                 round(weather_forecast_item[1]["temperatureMax"]),
                                                 round(weather_forecast_item[1]["temperatureMin"]),
                                                 emoji1=_weather_emojis["temperatureMax"],
                                                 emoji2=_weather_emojis["temperatureMin"]) for
                            weather_forecast_item in weather_list[1:]]
                           )

    return '\n'.join(weather_summary)


class WeatherParser:
    @classmethod
    def structured_weather_forecast(cls, weather_forecast):
        return _structured_weather_forecast(weather_forecast)

    @classmethod
    def print_weather_forecast(cls, weather_forecast):
        return _print_weather_forecast(weather_forecast)

    @classmethod
    def print_weather_forecast_item(cls, weather_forecast_item, location=None):
        return _print_weather_forecast_item(weather_forecast_item, location)
