class Config(object):
	LOGGER = False
	# Must be filled!
	# Register here: https://my.telegram.org/apps
	api_id = 123
	api_hash = ""
	DB_URI = "postgres://nanauser:nanapw@localhost:5432/nanadb"  # Your database URL
	PM_PERMIT = True
	# Version
	lang_code = "en"  # Your language code

	# Use real bot for Assistant
	# Pass False if you dont want
	ASSISTANT_BOT = True
	ASSISTANT_BOT_TOKEN = ""

	# Required for some features
	AdminSettings = ""  # Add someone id telegram, so they can access your assistant,separate with spaces, leave it blank if you dont want!
	Command = "! ."  # Insert command prefix, separate with space, if you insert "!" then you can do !ping
	TG_USERNAME = "@blablabla" # Insert Your Telegram Username
	# WORKER must be int (number)
	NANA_WORKER = 8
	ASSISTANT_WORKER = 2
	# If True, send notification to user if Official branch has new update after running bot
	REMINDER_UPDATE = True

	# APIs token
	thumbnail_API = ""  # Register free here: https://thumbnail.ws/
	screenshotlayer_API = ""  # Register free here: https://screenshotlayer.com/
	bitly_token = ""  # register here : bitly.com
	lydia_api = ""  # register here : https://coffeehouse.intellivoid.info/
	HEROKU_API = ""  # if you're using heroku this field must filled, get from here : https://dashboard.heroku.com/account

	# Last Fm API
	lastfm_api = ""
	lastfm_username = ""

	# Remove Bg API
	remove_bg_api = ""

	# Spotify API

	CLIENT_ID_SPOTIFY = ""
	CLIENT_SECRET_SPOTIFY = ""
	SPOTIFY_USERNAME = ""
	SPOTIFY_INITIAL_TOKEN = ""

	# Load or no load plugins
	# Separate Name With Spaces
	# userbot

	USERBOT_LOAD = ""
	USERBOT_NOLOAD = ""

	# manager

	ASSISTANT_LOAD = ""
	ASSISTANT_NOLOAD = ""

	# Fill this if you want to login using session code, else leave it blank
	USERBOT_SESSION = ""
	ASSISTANT_SESSION = ""

	# Pass True if you want to use test mode
	TEST_MODE = False

	# test var config
	BINDERBYTE_API = ""

class Production(Config):
	LOGGER = False


class Development(Config):
	TEST_DEVELOP = None
	LOGGER = False
	TERMUX_USER = False
