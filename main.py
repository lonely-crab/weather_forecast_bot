from bot.bot import start_bot
from database.database_orm import create_models

if __name__ == '__main__':
    create_models()
    start_bot()

