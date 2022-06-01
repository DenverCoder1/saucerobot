"""
config.py - Configuration of environment variables for the bot.
"""

import os
from dotenv import load_dotenv

load_dotenv()

SAUCENAO_API_KEY = os.getenv("SAUCENAO_API_KEY")
