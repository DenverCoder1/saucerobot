"""
bot.py - Main file for the reddit bot, the Bot class is exported for running the bot from the module.

Run the bot with `python -m reddit_bot`
"""

import asyncio
import logging
import urllib.parse
from math import floor
from typing import Optional

import asyncpraw
import asyncpraw.exceptions
import config
import yarl
from saucenao_api import AIOSauceNao
from table2ascii import PresetStyle, table2ascii

logging.basicConfig(level=logging.INFO)


class SauceBot:
    """
    Bot class for interacting with the reddit API.
    """

    def __init__(self):
        """Initialize the bot."""
        # seconds to wait between checking for new comments
        self.COMMENT_CHECK_INTERVAL = 10
        # minimum similarity required to include in the reply
        self.SIMILARITY_THRESHOLD = 75
        # set of seen comment ids
        self.seen: set[str] = set()

        self.reddit = asyncpraw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            user_agent=f"u/{config.REDDIT_USERNAME} by u/{config.REDDIT_BOT_AUTHOR}",
            username=config.REDDIT_USERNAME,
            password=config.REDDIT_PASSWORD,
        )
        self.saucenao = AIOSauceNao(config.SAUCENAO_API_KEY)
        self.me: Optional[asyncpraw.reddit.Redditor] = None

    def should_process_comment(self, comment: asyncpraw.reddit.Comment) -> bool:
        """Determines whether or not a comment should be processed."""
        return (
            comment.author != self.me
            and comment.author.name != "AutoModerator"
            and not comment.saved
        )

    async def save_comment(self, comment: asyncpraw.reddit.Comment):
        """Saves a comment to the seen set and marks it as saved on Reddit."""
        self.seen.add(comment.id)
        await comment.save()

    async def process_mentions(self):
        """Process Reddit comments containing mentions and replies to them with the results."""
        async for comment in self.reddit.inbox.mentions():
            if comment.id in self.seen:
                continue

            # refresh to get additional information such as whether or not the comment is saved
            comment: asyncpraw.reddit.Comment = await comment.refresh()

            if not self.should_process_comment(comment):
                self.seen.add(comment.id)
                continue

            sauce = await self.build_reply(comment)
            if sauce is not None:
                await comment.reply(sauce)
                logging.info(
                    f"Replied to {comment.author.name} https://reddit.com{comment.permalink}"
                )
            await self.save_comment(comment)

    def image_search_links(self, image_url: str) -> dict[str, str]:
        """Generates the links to search for the image on multiple sites."""
        encoded_url = urllib.parse.quote_plus(image_url)
        return {
            "SauceNAO": f"https://saucenao.com/search.php?db=999&url={encoded_url}",
            "Google Images": f"https://www.google.com/searchbyimage?image_url={encoded_url}&safe=off",
            "IQDB": f"https://iqdb.org/?url={encoded_url}",
            "TinEye": f"https://www.tineye.com/search/?url={encoded_url}",
            "Trace.moe": f"https://trace.moe/?auto&url={encoded_url}",
            "Ascii2d": f"https://ascii2d.net/search/url/{encoded_url}",
            "Yandex": f"https://yandex.com/images/search?rpt=imageview&url={encoded_url}",
        }

    def feedback_link(self):
        """Returns the link to compose a feedback message to the bot."""
        assert self.me is not None
        return f"https://www.reddit.com/message/compose/?to={self.me.name}"

    def source_link(self):
        """Returns the link to the source code."""
        return "https://github.com/DenverCoder1/saucerobot"

    def get_domain(self, url: str) -> str:
        """Returns the domain of a url (e.g. https://google.com/ -> google.com)."""
        parsed = yarl.URL(url)
        domain = parsed.host if parsed.host else url
        return domain.replace("www.", "", 1)

    async def build_reply(self, comment: asyncpraw.reddit.Comment) -> Optional[str]:
        """Builds the reply to a comment.

        Returns:
            The reply to the comment, or None if the bot should not reply.
        """
        # load the submission to get the image url
        await comment.submission.load()
        parent_post_url = comment.submission.url
        # skip if the parent post is a self post
        if "/r/" in parent_post_url:
            logging.info(f"Skipping since it is in a self post. {parent_post_url}")
            return None
        # fetch sauce
        async with self.saucenao as saucenao:
            results = await saucenao.from_url(parent_post_url)
        # build reply from results
        search_links = self.image_search_links(parent_post_url)
        reply = f"Here are the results from [SauceNAO]({search_links['SauceNAO']}):\n\n"
        result_table = [
            [
                f"**{result.title}** by {result.author}",
                f"[{self.get_domain(result.urls[0])}]({result.urls[0]})",
                f"{floor(result.similarity)}%",
            ]
            for result in results
            if result.similarity > self.SIMILARITY_THRESHOLD
        ]
        # no results
        if len(result_table) == 0:
            logging.info(f"No results found. https://reddit.com{comment.permalink}")
            return None
        reply += table2ascii(
            header=["Title", "Link", "Similarity"],
            body=result_table,
            style=PresetStyle.markdown,
        )
        # add search links (\u00B7 is a middle dot)
        reply += "\n\n" + " \u00B7 ".join(
            f"[{name}]({url})" for name, url in search_links.items()
        )
        # add feedback link
        reply += f"\n\n[Source Code]({self.source_link()}) \u00B7 [Feedback]({self.feedback_link()})"
        return reply

    async def start(self):
        """Starts the bot."""
        self.me = await self.reddit.user.me()
        print(f"Logging in as {self.me}")

        while True:
            try:
                await self.process_mentions()
                await asyncio.sleep(self.COMMENT_CHECK_INTERVAL)
            except Exception as e:
                logging.error(e)
                await asyncio.sleep(self.COMMENT_CHECK_INTERVAL)
