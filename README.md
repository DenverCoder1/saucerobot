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

### SauceNAO API

Create a copy of `.env.example` and name it `.env`

In the `.env` file, you must set the following environment variables:

* `SAUCENAO_API_KEY` - Your SauceNAO API key

To receive your SauceNAO API key, visit [SauceNAO](https://saucenao.com/user.php) to log in or create an account, then select the [API](https://saucenao.com/user.php?page=search-api) tab.

### Reddit Bot

Create a copy of `praw.ini.example` and name it `praw.ini`

In the `praw.ini` file, you must set the following variables under the `[saucerobot]` section:

* `username` - Your bot's username
* `password` - Your bot's password
* `client_id` - Your bot's client ID
* `client_secret` - Your bot's client secret

To obtain the client ID and client secret, visit [Reddit App Preferences](https://www.reddit.com/prefs/apps/) and create a new application while signed in as your bot.
