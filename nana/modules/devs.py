import os
import re
import shutil
import subprocess
import sys
import traceback
from platform import python_version

import requests
from pyrogram import Filters
from speedtest import Speedtest
import pyrogram as p

from nana import Command, logging, app, DB_AVAILABLE, USERBOT_VERSION, ASSISTANT_VERSION
from nana.helpers.deldog import deldog
from nana.helpers.parser import mention_markdown

__MODULE__ = "Devs"
__HELP__ = """
This command means for helping development

──「 **Execution** 」──
-> `exec (command)`
Execute a python commands.

──「 **Evaluation** 」──
-> `eval (command)`
Do math evaluation.

──「 **Command shell** 」──
-> `cmd (command)`
Execute command shell

──「 **Take log** 」──
-> `log`
Edit log message, or deldog instead

──「 **Get Data Center** 」──
-> `dc`
Get user specific data center

──「 **Get Repo Nana-Bot** 」──
-> `repo`
Get Repo For this userbot

──「 **Test Your Server Internet Speed** 」──
-> `speedtest`
Obtain Server internet speed using speedtest

──「 **Get ID** 」──
-> `id`
Send id of what you replied to

"""


async def stk(chat, photo):
    if "http" in photo:
        r = requests.get(photo, stream=True)
        with open("nana/cache/stiker.png", "wb") as stk:
            shutil.copyfileobj(r.raw, stk)
        await app.send_sticker(chat, "nana/cache/stiker.png")
        os.remove("nana/cache/stiker.png")
    else:
        await app.send_sticker(chat, photo)


async def vid(chat, video, caption=None):
    await app.send_video(chat, video, caption)


async def pic(chat, photo, caption=None):
    await app.send_photo(chat, photo, caption)


async def aexec(client, message, code):
    # Make an async function with the code and `exec` it
    exec(
        'async def __ex(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )

    # Get `__ex` from local variables, call it and return the result
    return await locals()['__ex'](client, message)


@app.on_message(Filters.me & Filters.command(["exec"], Command))
async def executor(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `exec message.edit('edited!')`")
        return
    args = message.text.split(None, 1)
    code = args[1]
    try:
        await aexec(client, message, code)
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
        await message.edit("**Execute**\n`{}`\n\n**Failed:**\n```{}```".format(code, "".join(errors)))
        logging.exception("Execution error")


@app.on_message(Filters.me & Filters.command(["ip"], Command))
async def public_ip(_client, message):
    ip = requests.get('https://api.ipify.org').text
    await message.edit(f'<code>{ip}</code>', parse_mode='html')


@app.on_message(Filters.me & Filters.command(["cmd"], Command))
async def terminal(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `cmd ping -c 5 google.com`")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception as err:
                await message.edit("""
**Input:**
```{}```

**Error:**
```{}```
""".format(teks, err))
            output += "**{}**\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
            await message.edit("""**Input:**\n```{}```\n\n**Error:**\n```{}```""".format(teks, "".join(errors)))
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            file = open("nana/cache/output.txt", "w+")
            file.write(output)
            file.close()
            await client.send_document(message.chat.id, "nana/cache/output.txt", reply_to_message_id=message.message_id,
                                       caption="`Output file`")
            os.remove("nana/cache/output.txt")
            return
        await message.edit("""**Input:**\n```{}```\n\n**Output:**\n```{}```""".format(teks, output))
    else:
        await message.edit("**Input: **\n`{}`\n\n**Output: **\n`No Output`".format(teks))


@app.on_message(Filters.me & Filters.command(["log"], Command))
async def log(_client, message):
    f = open("nana/logs/error.log", "r")
    data = await deldog(message, f.read())
    await message.edit("`Your recent logs stored here : `{}".format(data))


@app.on_message(Filters.me & Filters.command(["dc"], Command))
async def dc_id(_client, message):
    user = message.from_user
    if message.reply_to_message:
        if message.reply_to_message.forward_from:
            dc_id = message.reply_to_message.forward_from.dc_id
            user = mention_markdown(message.reply_to_message.forward_from.id,
                                    message.reply_to_message.forward_from.first_name)
        else:
            dc_id = message.reply_to_message.from_user.dc_id
            user = mention_markdown(message.reply_to_message.from_user.id,
                                    message.reply_to_message.from_user.first_name)
    else:
        dc_id = user.dc_id
        user = mention_markdown(message.from_user.id, message.from_user.first_name)
    if dc_id == 1:
        text = "{}'s assigned datacenter is **DC1**, located in **MIA, Miami FL, USA**".format(user)
    elif dc_id == 2:
        text = "{}'s assigned datacenter is **DC2**, located in **AMS, Amsterdam, NL**".format(user)
    elif dc_id == 3:
        text = "{}'s assigned datacenter is **DC3**, located in **MIA, Miami FL, USA**".format(user)
    elif dc_id == 4:
        text = "{}'s assigned datacenter is **DC4**, located in **AMS, Amsterdam, NL**".format(user)
    elif dc_id == 5:
        text = "{}'s assigned datacenter is **DC5**, located in **SIN, Singapore, SG**".format(user)
    else:
        text = "{}'s assigned datacenter is **Unknown**".format(user)
    await message.edit(text)


@app.on_message(Filters.me & Filters.command(["repo"], Command))
async def repo(_client, message):
    await message.edit(
        "Click [here](https://github.com/legenhand/Nana-Bot) for Nana-Bot-Remix Source.\nClick [here](https://github.com/legenhand/Nana-Bot) to open Nana-Bot GitHub page.\nClick [here](https://t.me/nanabotsupport) for support Group",
        disable_web_page_preview=True)


@app.on_message(Filters.me & Filters.command(["alive"], Command))
async def alive(_client, message):
    try:
        me = await app.get_me()
    except ConnectionError:
        me = None
    text = "Hello {}!\n".format(message.from_user.first_name)
    text += "**Here is your current stats:**\n"
    if not me:
        text += "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
    else:
        text += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
    text += "-> Assistant: `Running (v{})`\n".format(ASSISTANT_VERSION)
    text += "-> Database: `{}`\n".format(DB_AVAILABLE)
    text += "-> Python: `{}`\n".format(python_version())
    text += "-> Pyrogram: `{}`\n".format(p.__version__)
    if not me:
        text += "\nBot is currently turned off, to start bot again, type /settings and click **Start Bot** button"
    else:
        text += "\nBot logged in as `{}`\n Go to your assistant for more information!".format(me.first_name)
    await message.edit(text)

@app.on_message(Filters.me & Filters.command(["id"], Command))
async def get_id(_client, message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message
        if rep.audio:
            file_id = rep.audio.file_id
        elif rep.document:
            file_id = rep.document.file_id
        elif rep.photo:
            file_id = rep.photo.file_id
        elif rep.sticker:
            file_id = rep.sticker.file_id
        elif rep.video:
            file_id = rep.video.file_id
        elif rep.animation:
            file_id = rep.animation.file_id
        elif rep.voice:
            file_id = rep.voice.file_id
        elif rep.video_note:
            file_id = rep.video_note.file_id
        elif rep.contact:
            file_id = rep.contact.file_id
        elif rep.location:
            file_id = rep.location.file_id
        elif rep.venue:
            file_id = rep.venue.file_id
        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        await message.edit(user_id)
    elif file_id:
        await message.edit(file_id)
    else:
        await message.edit("This chat's ID:\n`{}`".format(message.chat.id))


@app.on_message(Filters.me & Filters.command(["speedtest"], Command))
async def speedtest(_client, message):
    await message.edit("`Running speed test . . .`")
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    test.results.share()
    result = test.results.dict()
    await message.edit("`"
                       "Started at "
                       f"{result['timestamp']} \n\n"
                       "Download "
                       f"{speed_convert(result['download'])} \n"
                       "Upload "
                       f"{speed_convert(result['upload'])} \n"
                       "Ping "
                       f"{result['ping']} \n"
                       "ISP "
                       f"{result['client']['isp']}"
                       "`")


def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"
