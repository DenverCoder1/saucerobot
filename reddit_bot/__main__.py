"""
saucerobot - A reddit bot that fetches the sauce of images
"""

from .bot import SauceBot
import asyncio

if __name__ == "__main__":
    bot = SauceBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.start())
    loop.close()
