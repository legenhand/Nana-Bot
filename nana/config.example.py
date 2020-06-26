# Buat file config.py baru dalam dir dan impor yang sama, kemudian perpanjang kelas ini.
class Config(object):
	LOGGER = True
	# Must be filled!
	# Register here: https://my.telegram.org/apps
	api_id = 1234 # Your API_ID
	api_hash = "" # Your API_HASH
	DATABASE_URL = ""  # Your database URL

	# Version
	lang_code = "en"  # Your language code
	device_model = "PC"  # Device model
	system_version = "Linux"  # OS system type

	# Use real bot for Assistant
	# Pass False if you dont want
	ASSISTANT_BOT = True
	ASSISTANT_BOT_TOKEN = ""
	NANA_IMG = ""
	# Required for some features
	AdminSettings = []  # Insert int id, Add someone so they can access your assistant, leave it blank if you dont want!
	Command = ["!", "."]  # Insert command prefix, if you insert "!" then you can do !ping
	# WORKER must be int (number)
	NANA_WORKER = 8
	ASSISTANT_WORKER = 2
	# If True, send notification to user if Official branch has new update after running bot
	REMINDER_UPDATE = True

	# APIs token
	thumbnail_API = ""  # Register free here: https://thumbnail.ws/
	screenshotlayer_API = ""  # Register free here: https://screenshotlayer.com/
	bitly_token = ""  # register here : bitly.com
	lydia_api = ""
	lastfm_api = ""
	lastfm_username = ""
	remove_bg_api = ""
	HEROKU_API = ""  # if you're using heroku this field must filled, get from here : https://dashboard.heroku.com/account

	# Last Fm API
	lastfm_api = ""
	lastfm_username = ""

	# Remove Bg API
	remove_bg_api = ""

	# Load or no load plugins
	# userbot

	USERBOT_LOAD = []
	USERBOT_NOLOAD = []

	# manager bot

	ASSISTANT_LOAD = []
	ASSISTANT_NOLOAD = []

	# Fill this if you want to login using session code, else leave it blank
	USERBOT_SESSION = ""
	ASSISTANT_SESSION = ""
	# Pass True if you want to use test mode
	TEST_MODE = False


class Production(Config):
	LOGGER = False


class Development(Config):
	TEST_DEVELOP = None
	LOGGER = False
	TERMUX_USER = False
