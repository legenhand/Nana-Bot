import re
import time
import heroku3
import asyncio
import os
import requests
import math

from nana.__main__ import HELP_COMMANDS
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton

from nana import HEROKU_API
from nana import setbot, AdminSettings, Command, BotName, DB_AVAIABLE
from nana.__main__ import get_runtime
from nana.helpers.misc import paginate_modules
from nana.modules.chats import get_msgc

if DB_AVAIABLE:
    from nana.modules.database.chats_db import get_all_chats

Heroku = heroku3.from_key(HEROKU_API)
heroku_api = "https://api.heroku.com"

HELP_STRINGS = f"""
Hello! I am {BotName}, your Assistant!
I can help you for many things.

**Main** commands available::
 - /start: get your bot status
 - /stats: get your userbot status
 - /settings: settings your userbot
 - /getme: get your userbot profile info
 - /help: get all modules help

You can use {", ".join(Command)} on your userbot to execute that commands.
Here is current modules you have
"""


async def help_parser(client, chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help"))
    await client.send_message(chat_id, text, reply_markup=keyboard)


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["help"]))
async def help_command(client, message):
    if message.chat.type != "private":
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Bantuan", url=f"t.me/{setbot.get_me()['username']}?start=help")]])
        await message.reply("Hubungi saya di PM untuk mendapatkan daftar perintah.", reply_markup=keyboard)
        return
    await help_parser(client, message.chat.id, HELP_STRINGS)


def help_button_callback(_, query):
    if re.match(r"help_", query.data):
        return True


help_button_create = Filters.create(help_button_callback)


@setbot.on_callback_query(help_button_create)
async def help_button(_client, query):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    if True:
        if mod_match:
            module = mod_match.group(1)
            text = "This is help for the module **{}**:\n".format(HELP_COMMANDS[module].__MODULE__) \
                   + HELP_COMMANDS[module].__HELP__

            await query.message.edit(text=text,
                                     reply_markup=InlineKeyboardMarkup(
                                         [[InlineKeyboardButton(text="⬅️ Back", callback_data="help_back")]]))

        elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_text(text=HELP_STRINGS,
                                          reply_markup=InlineKeyboardMarkup(
                                              paginate_modules(curr_page - 1, HELP_COMMANDS, "help")))

        elif next_match:
            next_page = int(next_match.group(1))
            await query.message.edit(text=HELP_STRINGS,
                                     reply_markup=InlineKeyboardMarkup(
                                         paginate_modules(next_page + 1, HELP_COMMANDS, "help")))

        elif back_match:
            await query.message.edit(text=HELP_STRINGS,
                                     reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELP_COMMANDS, "help")))


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["stats"]))
async def stats(_client, message):
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/80.0.3987.149 Mobile Safari/537.36'
        )
    user_id = Heroku.account().id
    headers = {
    'User-Agent': useragent,
    'Authorization': f'Bearer {HEROKU_API}',
    'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    """ - Current - """
    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    text = "**Here is your current stats**\n"
    text += "Notes: `0 notes`\n"
    if DB_AVAIABLE:
        text += "Group joined: `{} groups`\n".format(len(get_all_chats()))
    text += "Message received: `{} messages`\n".format(get_msgc())

    a = await get_runtime()
    b = int(time.time())
    c = b - a
    month = c // 2678400
    days = c // 86400
    hours = c // 3600 % 24
    minutes = c // 60 % 60
    seconds = c % 60

    alivetext = ""
    if month:
        alivetext += "{} month, ".format(month)
    if days:
        alivetext += "{} days, ".format(days)
    if hours:
        alivetext += "{} hours, ".format(hours)
    if minutes:
        alivetext += "{} minutes, ".format(minutes)
    if seconds:
        alivetext += "{} seconds".format(seconds)

    text = f" -> `Dyno usage:`{AppHours}`**h** `{AppMinutes}`**m**"
    text += f"**|**  [`{AppPercentage}`**%**]"
    text += "\n\n"
    text += " -> `Dyno hours quota remaining this month`:`{hours}`**h**  `{minutes}`**m**  "
    text += f"**|**  [`{percentage}`**%**]"

    text += "\nBot was alive for `{}`".format(alivetext)
    await message.reply_text(text, quote=True)
