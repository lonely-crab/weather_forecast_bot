import requests
from config_data.config import GET_IP_LINK


def _get_ip() -> str:
    response = requests.get(GET_IP_LINK)
    if response.status_code == 200:
        return response.text
    else:
        return ""


class GetIpInterface:
    @classmethod
    def get_ip(cls) -> str:
        if not _get_ip():
            raise ValueError("Couldn't get ip from API.")
        return _get_ip()


if __name__ == '__main__':
    _get_ip()
    GetIpInterface()
    print(GetIpInterface().get_ip())