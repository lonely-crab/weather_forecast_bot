import requests
from config import API_KEY_IP, API_HOST_IP
from get_ip import GetIpInterface


def _get_location() -> dict:
    try:
        ip = GetIpInterface.get_ip()
    except ValueError:
        return {}
    headers = {
        "X-RapidAPI-Key": API_KEY_IP,
        "X-RapidAPI-Host": API_HOST_IP
    }
    params = {
        "ip-or-hostname": ip
    }
    response = requests.get("https://{host}/json/{ip}".format(host=API_HOST_IP, ip=ip), headers=headers, params=params)
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


if __name__ == '__main__':
    _get_location()
    GetLocationInterface()

