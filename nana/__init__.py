import logging
import os
import sys
import time

from pydrive.auth import GoogleAuth
from pyrogram import Client, errors
from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

StartTime = time.time()

# Postgresql

# logging
# 
# -> Advanced logging, for debugging purposes

#
ENV = bool(os.environ.get('ENV', False))
if ENV:
    TEST_DEVELOP = bool(os.environ.get('TEST_DEVELOP', False))
else:
    try:
        from nana.config import Development as Config
    except ModuleNotFoundError:
        logging.error("You need to place config.py in nana dir!")
        quit(1)
    TEST_DEVELOP = Config.TEST_MODE

if TEST_DEVELOP:
    logging.warning("Testing mode activated!")
    log = logging.getLogger()

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    logging.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
    quit(1)

USERBOT_VERSION = "1.1.1b"
ASSISTANT_VERSION = "1.1.1b"

OFFICIAL_BRANCH = ('master', 'dev', 'asyncio')
REPOSITORY = "https://github.com/legenhand/Nana-Bot.git"
RANDOM_STICKERS = ["CAADAgAD6EoAAuCjggf4LTFlHEcvNAI", "CAADAgADf1AAAuCjggfqE-GQnopqyAI",
                   "CAADAgADaV0AAuCjggfi51NV8GUiRwI"]

BOT_SESSION = "nana/session/ManageBot"
APP_SESSION = "nana/session/Nana"

if ENV:
    # Logger
    logger = os.environ.get('LOGGER', False)
    # Version
    lang_code = os.environ.get('lang_code', "en")
    device_model = os.environ.get('device_model', "PC")
    app_version = "💝 Nana v{}".format(USERBOT_VERSION)
    system_version = os.environ.get('system_version', "Linux")

    # Must be filled
    api_id = os.environ.get('api_id', None)
    api_hash = os.environ.get('api_hash', None)

    # Session
    USERBOT_SESSION = os.environ.get('USERBOT_SESSION', None)
    ASSISTANT_SESSION = os.environ.get('ASSISTANT_SESSION', None)

    # Required for some features
    # Set temp var for load later
    Owner = 0
    OwnerName = ""
    OwnerUsername = ""
    BotID = 0
    BotName = ""
    BotUsername = ""
    # From config
    Command = os.environ.get("Command", "! . - ^").split()
    NANA_WORKER = int(os.environ.get('NANA_WORKER', 8))
    ASSISTANT_WORKER = int(os.environ.get('ASSISTANT_WORKER', 2))

    try:
        TEST_DEVELOP = bool(os.environ.get('TEST_DEVELOP', False))
        if TEST_DEVELOP:
            BOT_SESSION = os.environ.get('BOT_SESSION', None)
            APP_SESSION = os.environ.get('APP_SESSION', None)
        else:
            raise AttributeError
    except AttributeError:
        pass

    # APIs
    thumbnail_API = os.environ.get('thumbnail_API', None)
    screenshotlayer_API = os.environ.get('screenshotlayer_API', None)
    bitly_token = [os.environ.get('bitly_token', None)]
    gdrive_credentials = os.environ.get('gdrive_credentials', None)
    lydia_api = os.environ.get('lydia_api', None)
    lastfm_api = os.environ.get('lastfm_api', None)
    remove_bg_api = os.environ.get('remove_bg_api', None)
    lastfm_username = os.environ.get('lastfm_username', None)
    HEROKU_API = os.environ.get('HEROKU_API', None)
    # LOADER
    USERBOT_LOAD = os.environ.get("USERBOT_LOAD", "").split()
    USERBOT_NOLOAD = os.environ.get("USERBOT_NOLOAD", "").split()
    ASSISTANT_LOAD = os.environ.get("ASSISTANT_LOAD", "").split()
    ASSISTANT_NOLOAD = os.environ.get("ASSISTANT_NOLOAD", "").split()

    DATABASE_URL = os.environ.get('DATABASE_URL', "postgres://username:password@localhost:5432/database")
    ASSISTANT_BOT_TOKEN = os.environ.get('ASSISTANT_BOT_TOKEN', None)
    AdminSettings = [int(x) for x in os.environ.get("AdminSettings", "").split()]
    REMINDER_UPDATE = bool(os.environ.get('REMINDER_UPDATE', True))
    TEST_MODE = bool(os.environ.get('TEST_MODE', False))
    TG_USERNAME = os.environ.get('TG_USERNAME', None)
else:
    # logger
    logger = Config.LOGGER
    # Version
    lang_code = Config.lang_code
    device_model = Config.device_model
    app_version = "💝 Nana v{}".format(USERBOT_VERSION)
    system_version = Config.system_version

    # Must be filled
    api_id = Config.api_id
    api_hash = Config.api_hash

    # Session
    USERBOT_SESSION = Config.USERBOT_SESSION
    ASSISTANT_SESSION = Config.ASSISTANT_SESSION
    TG_USERNAME = Config.TG_USERNAME
    # Required for some features
    # Set temp var for load later
    Owner = 0
    OwnerName = ""
    OwnerUsername = ""
    BotID = 0
    BotName = ""
    BotUsername = ""
    # From config
    Command = Config.Command
    NANA_WORKER = Config.NANA_WORKER
    ASSISTANT_WORKER = Config.ASSISTANT_WORKER

    # APIs
    thumbnail_API = Config.thumbnail_API
    screenshotlayer_API = Config.screenshotlayer_API
    bitly_token = [Config.bitly_token]
    gdrive_credentials = None
    lydia_api = Config.lydia_api
    HEROKU_API = Config.HEROKU_API
    lastfm_api = Config.lastfm_api
    remove_bg_api = Config.remove_bg_api
    lastfm_username = Config.lastfm_username
    # LOADER
    USERBOT_LOAD = Config.USERBOT_LOAD
    USERBOT_NOLOAD = Config.USERBOT_NOLOAD
    ASSISTANT_LOAD = Config.ASSISTANT_LOAD
    ASSISTANT_NOLOAD = Config.ASSISTANT_NOLOAD

    DATABASE_URL = Config.DATABASE_URL
    ASSISTANT_BOT_TOKEN = Config.ASSISTANT_BOT_TOKEN
    AdminSettings = Config.AdminSettings
    REMINDER_UPDATE = Config.REMINDER_UPDATE
    TEST_MODE = Config.TEST_MODE
if os.path.exists("nana/logs/error.log"):
    f = open("nana/logs/error.log", "w")
    f.write("PEAK OF THE LOGS FILE")
LOG_FORMAT = "[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)s %(levelname)s: %(message)s"
logging.basicConfig(level=logging.ERROR,
                    format=LOG_FORMAT,
                    datefmt='%m-%d %H:%M',
                    filename='nana/logs/error.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter(LOG_FORMAT)
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

log = logging.getLogger()
log.error("THIS IS PEAK OF LOG ERROR, IGNORE THIS MESSAGE LOG")

if USERBOT_SESSION and ASSISTANT_SESSION:
    BOT_SESSION = ASSISTANT_SESSION
    APP_SESSION = USERBOT_SESSION

gauth = GoogleAuth()

DB_AVAILABLE = False
BOTINLINE_AVAIABLE = False


# Postgresql
def mulaisql() -> scoped_session:
    global DB_AVAILABLE
    engine = create_engine(DATABASE_URL, client_encoding="utf8")
    BASE.metadata.bind = engine
    try:
        BASE.metadata.create_all(engine)
    except exc.OperationalError:
        DB_AVAILABLE = False
        return False
    DB_AVAILABLE = True
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


async def get_bot_inline(bot):
    global BOTINLINE_AVAIABLE
    if setbot:
        try:
            await app.get_inline_bot_results("@{}".format(bot.username), "test")
            BOTINLINE_AVAIABLE = True
        except errors.exceptions.bad_request_400.BotInlineDisabled:
            BOTINLINE_AVAIABLE = False


async def get_self():
    global Owner, OwnerName, OwnerUsername, AdminSettings
    getself = await app.get_me()
    Owner = getself.id
    if getself.last_name:
        OwnerName = getself.first_name + " " + getself.last_name
    else:
        OwnerName = getself.first_name
    OwnerUsername = getself.username
    if Owner not in AdminSettings:
        AdminSettings.append(Owner)


async def get_bot():
    global BotID, BotName, BotUsername
    getbot = await setbot.get_me()
    BotID = getbot.id
    BotName = getbot.first_name
    BotUsername = getbot.username


BASE = declarative_base()
SESSION = mulaisql()

setbot = Client(BOT_SESSION, api_id=api_id, api_hash=api_hash, bot_token=ASSISTANT_BOT_TOKEN, workers=ASSISTANT_WORKER,
                test_mode=TEST_MODE)

app = Client(APP_SESSION, api_id=api_id, api_hash=api_hash, app_version=app_version, device_model=device_model,
             system_version=system_version, lang_code=lang_code, workers=NANA_WORKER, test_mode=TEST_MODE)
