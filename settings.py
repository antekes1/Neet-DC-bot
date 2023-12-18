import os
from dotenv import load_dotenv
from logging.config import dictConfig

load_dotenv()

Bot_token = str(os.getenv("BOT_API_TOKEN"))

LOGGING_CONFIG = {
    "ver": 1,
}