import requests
from config_data.config import API_HOST_WEATHER, API_KEY_WEATHER
from .get_loc_from_ip import GetLocationInterface


def _get_weather(timesteps: str = "1d", units: str = "metric") -> dict:
    try:
        location = GetLocationInterface.get_location()
    except ValueError:
        return {}

    headers = {
        "X-RapidAPI-Key": API_KEY_WEATHER,
        "X-RapidAPI-Host": API_HOST_WEATHER
    }
    params = {
        "location": ','.join([str(location['latitude']), str(location['longitude'])]),
        "timesteps": timesteps,
        "units": units
    }
    response = requests.get("https://{host}/v4/weather/forecast".format(host=API_HOST_WEATHER),
                            headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}
    
    
class GetWeatherInterface:
    @classmethod
    def get_weather(cls, timesteps: str = "1d", units: str = "metric") -> dict:
        if not _get_weather(timesteps, units):
            raise ValueError("Couldn't get weather from API.")
        return _get_weather(timesteps, units)


if __name__ == '__main__':
    _get_weather()
    GetWeatherInterface()
    print(_get_weather())
