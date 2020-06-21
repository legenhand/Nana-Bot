import re
import time

from __main__ import HELP_COMMANDS
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton

from nana import setbot, AdminSettings, Command, BotName, DB_AVAILABLE, StartTime
from nana.__main__ import get_runtime
from nana.helpers.misc import paginate_modules
from nana.modules.chats import get_msgc

if DB_AVAILABLE:
    from nana.modules.database.chats_db import get_all_chats

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


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

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
    text = "**Here is your current stats**\n"
    text += "Notes: `0 notes`\n"
    if DB_AVAILABLE:
        text += "Group joined: `{} groups`\n".format(len(get_all_chats()))
    text += "Message received: `{} messages`\n".format(get_msgc())

    uptime = get_readable_time((time.time() - StartTime))
    text += ("<b>Nana uptime:</b> <code>{}</code>".format(uptime))
    await message.reply_text(text, quote=True)
