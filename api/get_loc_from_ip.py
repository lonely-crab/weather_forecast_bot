import requests
from config import API_KEY_IP, API_HOST_IP
from .get_ip import GetIpInterface


def _get_location() -> dict:
    try:
        ip = GetIpInterface.get_ip()
    except ValueError:
        return {}

    params = {
        "ip": ip,
        "format": "json",
        "key": API_KEY_IP
    }
    response = requests.get("https://{host}/".format(host=API_HOST_IP), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {}


class GetLocationInterface:
    @classmethod
    def get_location(cls) -> dict:
        if not _get_location():
            raise ValueError("Couldn't get location from API.")
        return _get_location()

    def get_timezone(self):
        return self.get_location()['time_zone']


if __name__ == '__main__':
    _get_location()
    GetLocationInterface()
    print(GetLocationInterface().get_location())

