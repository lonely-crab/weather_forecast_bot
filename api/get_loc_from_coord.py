import requests
from requests.structures import CaseInsensitiveDict
from config_data.config import API_KEY_LOCATION, API_HOST_LOCATION
from database.redis_database import RedisDatabaseInterface


def _get_location(user_id, latitude, longitude) -> dict:
    url = "https://{host}/v1/geocode/reverse".format(host=API_HOST_LOCATION)

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    params = {
        "lat": latitude,
        "lon": longitude,
        "apiKey": API_KEY_LOCATION
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['features'][0]['properties']['datasource']
    else:
        raise ValueError("Couldn't get location from API.")


class GetLocationInterface:
    @classmethod
    def get_location(cls, user_id) -> dict:
        try:
            return _get_location(**RedisDatabaseInterface.get_redis(user_id, "location"))
        except ValueError as error:
            raise ValueError(str(error))
        except KeyError:
            raise ValueError("Location isn't set. Use /set_location command.")