import requests
from config_data.config import API_HOST_WEATHER, API_KEY_WEATHER
from database.redis_database import RedisDatabaseInterface


def _get_weather(
    user_id: str | int, timesteps: str = "1d", units: str = "metric"
) -> dict:
    """
    Get weather from API.
    :param user_id:
    :type user_id: str | int
    :param timesteps:
    :type timesteps: str
    :param units:
    :type units: str
    :return: weather dictionary
    :rtype: dict
    """
    try:
        location: dict = RedisDatabaseInterface.get_redis(user_id, "location")
    except (KeyError, TypeError):
        raise ValueError("Location isn't set. Use /set_location command.")
    try:
        location_query = ",".join(
            [str(location["latitude"]), str(location["longitude"])]
        )
    except (KeyError, TypeError):
        try:
            location_query = " ".join([location["country"], location["city"]])
        except (KeyError, TypeError):
            location_query = location
    headers = {
        "X-RapidAPI-Key": API_KEY_WEATHER,
        "X-RapidAPI-Host": API_HOST_WEATHER,
    }

    params = {
        "location": location_query,
        "timesteps": timesteps,
        "units": units,
    }
    response = requests.get(
        "https://{host}/v4/weather/forecast".format(host=API_HOST_WEATHER),
        headers=headers,
        params=params,
    )
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        raise ValueError(
            "It seems that your location isn't correct. Use /set_location command."
        )
    else:
        return {}


class GetWeatherInterface:
    """
    Class for getting weather from API.
    """

    @classmethod
    def get_weather(
        cls, user_id: str | int, timesteps: str = "1d", units: str = "metric"
    ) -> dict[str, list[dict[str, ...]]] | None:
        """
        Get weather from API.
        :param user_id:
        :type user_id: str | int
        :param timesteps:
        :type timesteps: str
        :param units:
        :type units: str
        :return: weather dictionary
        :rtype: dict
        """
        try:
            if not _get_weather(user_id, timesteps, units):
                raise ValueError(
                    "Couldn't get weather from API."
                    " Check if your location is correct or try locating differently."
                )
            return _get_weather(user_id, timesteps, units)
        except ValueError as error:
            raise ValueError(str(error))


if __name__ == "__main__":
    pass
