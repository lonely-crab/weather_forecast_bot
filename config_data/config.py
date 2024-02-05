import os
import dotenv


dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN отсутствует в переменных окружения")

API_KEY_LOCATION = os.getenv('API_KEY_LOCATION')
if not API_KEY_LOCATION:
    raise ValueError("API_KEY_LOCATION отсутствует в переменных окружения")

API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
if not API_KEY_WEATHER:
    raise ValueError("API_KEY_WEATHER отсутствует в переменных окружения")

API_HOST_WEATHER = "tomorrow-io1.p.rapidapi.com"
API_HOST_LOCATION = "api.geoapify.com"

# поддерживаемые команды
DEFAULT_COMMANDS = [
    ('start', 'Start bot'),
    ('current_weather', 'Get hourly weather forecast at your location'),
    ('weather_forecast', 'Get weather forecast for the next 6 days at your location (including today)'),
    ('help', 'List of commands and their descriptions'),
    ('custom', 'Custom weather forecast (try \\custom for more information)'),
    ('history', 'History of requests')
]


