from bot.bot import start_bot
from config import DEFAULT_COMMANDS
from database.database_orm import create_models
import json

if __name__ == '__main__':
    create_models()
    start_bot()

