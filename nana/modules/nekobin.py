import asyncio
from requests import get, post
from requests.exceptions import HTTPError, Timeout, TooManyRedirects
import os
from pyrogram import Filters, Message
from nana import Command, app

__MODULE__ = "Nekobin"
__HELP__ = """
──「 **Paste to Nekobin** 」──
-> `neko`
Create a Nekobin paste using replied to message.

"""

@app.on_message(Filters.me & Filters.command(["neko"], Command))
async def paste(client, message):
    cmd = message.command
    text = ""
    if len(cmd) > 1:
        text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Usage: `neko (reply to a text or a document)`")
        await asyncio.sleep(2)
        await message.delete()
        return
    replied = text
    use_neko = True
    file_ext = '.txt'
    if not text and replied and replied.document and replied.document.file_size < 2 ** 20 * 10:
        file_ext = os.path.splitext(replied.document.file_name)[1]
        path = await replied.download('/root/nana/')
        with open(path, 'r') as d_f:
            text = d_f.read()
        os.remove(path)
    elif not text and replied and replied.text:
        text = replied.text
    await message.edit("`Pasting text...`")
    resp = post("https://nekobin.com/" + "api/documents", json={"content": text})
    if resp.status_code == 201:
        response = resp.json()
        key = response['result']['key']
        final_url = "https://nekobin.com/" + key + file_ext
        reply_text = f"`Successfully pasted on` [Nekobin]({final_url})"
        await message.edit(reply_text, disable_web_page_preview=True)
    else:
        await message.edit("Failed to reach Nekobin")