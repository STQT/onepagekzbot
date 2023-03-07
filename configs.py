import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

BOT_TOKEN = os.getenv('BOT_TOKEN')

API_URL = os.getenv('API_URL')