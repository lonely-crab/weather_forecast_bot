import requests
from config_data.config import API_HOST_WEATHER, API_KEY_WEATHER
from database.redis_database import RedisDatabaseInterface


def _get_weather(user_id, timesteps: str = "1d", units: str = "metric") -> dict:
    try:
        location = RedisDatabaseInterface.get_redis(user_id, "location")
    except KeyError:
        raise ValueError("Location isn't set. Use /set_location command.")

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
    elif response.status_code == 400:
        raise ValueError("It seems that your location isn't correct. Use /set_location command.")
    else:
        return {}
    
    
class GetWeatherInterface:
    @classmethod
    def get_weather(cls,user_id, timesteps: str = "1d", units: str = "metric") -> dict:
        try:
            if not _get_weather(user_id, timesteps, units):
                raise ValueError("Couldn't get weather from API.")
            return _get_weather(user_id, timesteps, units)
        except ValueError as error:
            raise ValueError(str(error))


if __name__ == '__main__':
    _get_weather("123")
    GetWeatherInterface()
    print(_get_weather("123"))
