import requests
from requests.structures import CaseInsensitiveDict
from config_data.config import API_KEY_LOCATION, API_HOST_LOCATION
from database.redis_database import RedisDatabaseInterface


def _get_location(latitude: float, longitude: float) -> dict[str, ...]:
    """
    Get location from coordinates.
    :param latitude: latitude
    :type latitude: float
    :param longitude: longitude
    :type longitude: float
    :return: location
    :raise: ValueError
    :rtype: dict

    """
    url = "https://{host}/v1/geocode/reverse".format(host=API_HOST_LOCATION)

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    params = {"lat": latitude, "lon": longitude, "apiKey": API_KEY_LOCATION}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["features"][0]["properties"]
    else:
        raise ValueError("Couldn't get location from API.")


class GetLocationInterface:
    """
    Class for getting location from coordinates.
    """

    @classmethod
    def get_location(cls, user_id: str | int) -> dict:
        """
        Get location from coordinates.
        :param user_id:
        :type user_id: str | int
        :return: location
        :rtype: dict
        """
        try:
            return _get_location(
                **RedisDatabaseInterface.get_redis(user_id, "location")
            )
        except ValueError as error:
            raise ValueError(str(error))
        except KeyError:
            raise ValueError("Location isn't set. Use /set_location command.")


if __name__ == "__main__":
    pass
