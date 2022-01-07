import os
import re
import shutil
import subprocess
import sys
import traceback
from io import StringIO

import requests
from pyrogram import filters

from nana import Command, app, edrep, AdminSettings
from nana.helpers.aiohttp_helper import AioHttp
from nana.helpers.deldog import deldog
from nana.helpers.parser import mention_markdown

__MODULE__ = "Devs"
__HELP__ = """
This command means for helping development

──「 **Execution** 」──
-> `eval (command)`
Python Shell Execution

──「 **Command shell** 」──
-> `sh (command)`
Execute command shell

──「 **Take log** 」──
-> `log`
Edit log message, or deldog instead

──「 **Get Data Center** 」──
-> `dc`
Get user specific data center

──「 **Test Your Server Internet Speed** 」──
-> `speedtest`
Obtain Server internet speed using speedtest

──「 **Get ID** 」──
-> `id`
Send id of what you replied to

──「 **Self Destruct Reveal** 」──
-> `reveal` or `reveal self`
Reveal Self Destruct photo untouched, 'self' tag will reveal it in Saved Messages
"""


async def stk(chat, photo):
    if "http" in photo:
        r = requests.get(photo, stream=True)
        with open("nana/cache/stiker.png", "wb") as stikr:
            shutil.copyfileobj(r.raw, stikr)
        await app.send_sticker(chat, "nana/cache/stiker.png")
        os.remove("nana/cache/stiker.png")
    else:
        await app.send_sticker(chat, photo)


async def vid(chat, video, caption=None):
    await app.send_video(chat, video, caption)


async def pic(chat, photo, caption=None):
    await app.send_photo(chat, photo, caption)


async def aexec(code, client, message):
    exec(
        f'async def __aexec(client, message): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )
    return await locals()['__aexec'](client, message)


@app.on_message(filters.me & filters.command("reveal", Command))
async def sd_reveal(client, message):
    cmd = message.command
    self_tag = " ".join(cmd[1:])
    tags = "self" in self_tag
    if len(message.text.split()) == 1:
        await message.delete()
        return
    if tags:
        await message.delete()
        a = 'nana/file.png'
        await client.download_media(message.reply_to_message.photo, file_name=a)
        await client.send_photo('me', a)
        os.remove(a)
    else:
        await message.delete()
        a = 'nana/file.png'
        await client.download_media(message.reply_to_message.photo, file_name=a)
        await client.send_photo(message.chat.id, a)
        os.remove(a)


@app.on_message(filters.user(AdminSettings) & filters.command("eval", Command))
async def executor(client, message):
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await message.delete()
        return
    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"<b>QUERY</b>:\n<code>{cmd}</code>\n\n<b>OUTPUT</b>:\n<code>{evaluation.strip()}</code>"
    if len(final_output) > 4096:
        filename = 'output.txt'
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove(filename)
        await message.delete()
    else:
        await edrep(message, text=final_output)


@app.on_message(filters.user(AdminSettings) & filters.command("ip", Command))
async def public_ip(_client, message):
    j = await AioHttp().get_json("http://ip-api.com/json")
    stats = f"**ISP {j['isp']}:**\n"
    stats += f"**AS:** `{j['as']}`\n"
    stats += f"**IP Address:** `{j['query']}`\n"
    stats += f"**Country:** `{j['country']}`\n"
    stats += f"**Zip code:** `{j['zip']}`\n"
    stats += f"**Lattitude:** `{j['lat']}`\n"
    stats += f"**Longitude:** `{j['lon']}`\n"
    stats += f"**Time Zone:** `{j['timezone']}`"
    await edrep(message, text=stats, parse_mode='markdown')



@app.on_message(filters.user(AdminSettings) & filters.command("sh", Command))
async def terminal(client, message):
    if len(message.text.split()) == 1:
        await edrep(message, text="Usage: `sh ping -c 5 google.com`")
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
                print(err)
                await edrep(message, text="""
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
            await edrep(message, text="""**Input:**\n```{}```\n\n**Error:**\n```{}```""".format(teks, "".join(errors)))
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
        await edrep(message, text="""**Input:**\n```{}```\n\n**Output:**\n```{}```""".format(teks, output))
    else:
        await edrep(message, text="**Input: **\n`{}`\n\n**Output: **\n`No Output`".format(teks))


@app.on_message(filters.user(AdminSettings) & filters.command(["log"], Command))
async def log(_client, message):
    f = open("nana/logs/error.log", "r")
    data = await deldog(message, f.read())
    await edrep(message, text=f"`Your recent logs stored here : `{data}", disable_web_page_preview=True)


@app.on_message(filters.user(AdminSettings) & filters.command("dc", Command))
async def dc_id_check(_client, message):
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
    await edrep(message, text=text)


@app.on_message(filters.user(AdminSettings) & filters.command("id", Command))
async def get_id(_client, message):
    file_id = None
    user_id = None
    if message.reply_to_message:
        rep = message.reply_to_message
        if rep.audio:
            file_id = f"**File ID**: `{rep.audio.file_id}`\n"
            file_id += f"**File Ref**: `{rep.audio.file_ref}`\n"
            file_id += "**File Type**: `audio`\n"
        elif rep.document:
            file_id = f"**File ID**: `{rep.document.file_id}`\n"
            file_id += f"**File Ref**: `{rep.document.file_ref}`\n"
            file_id += f"**File Type**: `{rep.document.mime_type}`\n"
        elif rep.photo:
            file_id = f"**File ID**: `{rep.photo.file_id}`\n"
            file_id += f"**File Ref**: `{rep.photo.file_ref}`\n"
            file_id += "**File Type**: `photo`"
        elif rep.sticker:
            file_id = f"**Sicker ID**: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"**Sticker Set**: `{rep.sticker.set_name}`\n"
                file_id += f"**Sticker Emoji**: `{rep.sticker.emoji}`\n"
                if rep.sticker.is_animated:
                    file_id += f"**Animated Sticker**: `{rep.sticker.is_animated}`\n"
                else:
                    file_id += "**Animated Sticker**: `False`\n"
            else:
                file_id += "**Sticker Set**: __None__\n"
                file_id += "**Sticker Emoji**: __None__"
        elif rep.video:
            file_id = f"**File ID**: `{rep.video.file_id}`\n"
            file_id += f"**File Ref**: `{rep.video.file_ref}`\n"
            file_id += "**File Type**: `video`"
        elif rep.animation:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += f"**File Ref**: `{rep.animation.file_ref}`\n"
            file_id += "**File Type**: `GIF`"
        elif rep.voice:
            file_id = f"**File ID**: `{rep.voice.file_id}`\n"
            file_id += f"**File Ref**: `{rep.voice.file_ref}`\n"
            file_id += "**File Type**: `Voice Note`"
        elif rep.video_note:
            file_id = f"**File ID**: `{rep.animation.file_id}`\n"
            file_id += f"**File Ref**: `{rep.animation.file_ref}`\n"
            file_id += "**File Type**: `Video Note`"
        elif rep.location:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.location.latitude}`"
        elif rep.venue:
            file_id = "**Location**:\n"
            file_id += f"**longitude**: `{rep.venue.location.longitude}`\n"
            file_id += f"**latitude**: `{rep.venue.location.latitude}`\n\n"
            file_id += "**Address**:\n"
            file_id += f"**title**: `{rep.venue.title}`\n"
            file_id += f"**detailed**: `{rep.venue.address}`\n\n"
        elif rep.from_user:
            user_id = rep.from_user.id
    if user_id:
        if rep.forward_from:
            user_detail = f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.message_id}`"
        await edrep(message, text=user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = f"**Forwarded User ID**: `{message.reply_to_message.forward_from.id}`\n"
        else:
            user_detail = f"**User ID**: `{message.reply_to_message.from_user.id}`\n"
        user_detail += f"**Message ID**: `{message.reply_to_message.message_id}`\n\n"
        user_detail += file_id
        await edrep(message, text=user_detail)
    else:
        await edrep(message, text=f"**Chat ID**: `{message.chat.id}`")
