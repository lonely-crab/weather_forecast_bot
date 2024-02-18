import requests
from requests.structures import CaseInsensitiveDict
from config_data.config import API_KEY_LOCATION, API_HOST_LOCATION
from database.redis_database import RedisDatabaseInterface


def _get_time_zone(
    latitude: float = None,
    longitude: float = None,
    city: str = None,
    country: str = None,
) -> dict[str, ...]:
    if latitude and longitude:
        params = {
            "lat": latitude,
            "lon": longitude,
            "apiKey": API_KEY_LOCATION,
        }
        url = "https://{host}/v1/geocode/reverse".format(
            host=API_HOST_LOCATION
        )
    else:
        params = {"city": city, "country": country, "apiKey": API_KEY_LOCATION}
        url = "https://{host}/v1/geocode/search".format(host=API_HOST_LOCATION)
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["features"][0]["properties"]["timezone"][
            "offset_STD"
        ]
    else:
        raise ValueError("Couldn't get location from API.")


class GetTimeZoneInterface:
    @classmethod
    def get_time_zone(cls, user_id: str | int) -> None:
        try:
            RedisDatabaseInterface.set_redis(
                user_id,
                "timezone",
                _get_time_zone(
                    user_id,
                    **RedisDatabaseInterface.get_redis(user_id, "location")
                ),
            )
        except ValueError as error:
            raise ValueError(str(error))
        except KeyError:
            raise ValueError("Location isn't set. Use /set_location command.")


if __name__ == "__main__":
    pass
