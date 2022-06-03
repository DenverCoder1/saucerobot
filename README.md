# saucerobot

Bot for fetching image sources

![screenshot](https://user-images.githubusercontent.com/20955511/171333950-e9a6997e-c343-4aed-b14f-f59b048e5bc0.png)

## Running the bot

The Reddit bot can be launched using the command:

```py
python -m reddit_bot
```

The exact command may vary depending on your Operating System and Python installation.

## Configuration

Create a copy of `.env.example` and name it `.env`

In the `.env` file, you must set the following environment variables:

### SauceNAO API

* `SAUCENAO_API_KEY` - Your SauceNAO API key

To receive your SauceNAO API key, visit [SauceNAO](https://saucenao.com/user.php) to log in or create an account, then select the [API](https://saucenao.com/user.php?page=search-api) tab.

### Reddit Bot

* `REDDIT_USERNAME` - Your bot's Reddit username
* `REDDIT_PASSWORD` - Your bot's Reddit password
* `REDDIT_CLIENT_ID` - Your Reddit client ID
* `REDDIT_CLIENT_SECRET` - Your Reddit client secret
* `REDDIT_BOT_AUTHOR` - The author of the bot

To obtain the client ID and client secret, visit [Reddit App Preferences](https://www.reddit.com/prefs/apps/) and create a new application while signed in as your bot.
