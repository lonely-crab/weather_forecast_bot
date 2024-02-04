import os
import dotenv


dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN отсутствует в переменных окружения")

API_KEY_IP = os.getenv('API_KEY_IP')
if not API_KEY_IP:
    raise ValueError("API_KEY_IP отсутствует в переменных окружения")

API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
if not API_KEY_WEATHER:
    raise ValueError("API_KEY_WEATHER отсутствует в переменных окружения")

API_HOST_IP = "api.ip2location.io"
API_HOST_WEATHER = "tomorrow-io1.p.rapidapi.com"


# поддерживаемые команды
DEFAULT_COMMANDS = [
    ('start', 'Start bot'),
    ('current_weather', 'Get current weather at your location'),
    ('weather_forecast', 'Get weather forecast for the next 6 days at your location (including today)'),
    ('help', 'List of commands and their descriptions'),
    ('custom', 'Custom weather forecast (try \\custom for more information)'),
    ('history', 'History of requests')
]

GET_IP_LINK = "http://api.ipify.org/"

