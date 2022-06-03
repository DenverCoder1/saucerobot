"""
config.py - Configuration of environment variables for the bot.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# SauceNAO API key
SAUCENAO_API_KEY = os.getenv("SAUCENAO_API_KEY")

# Bot's reddit username (eg. saucerobot)
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "")

# Password for the bot's account (eg. password)
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "")

# Client ID for the bot from https://www.reddit.com/prefs/apps/ (eg. a1bC2DEFG51h3i_jKlMnop)
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")

# Client Secret for the bot from https://www.reddit.com/prefs/apps/ (eg. abc1dEfGhIjKlmNopQr2s_-t3Uvwx-yZ)
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")

# Bot author's username
REDDIT_BOT_AUTHOR = os.getenv("REDDIT_BOT_AUTHOR", "")
