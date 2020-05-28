import asyncio
import requests

from pyrogram import Filters, Message
from nana import Command, app

__MODULE__ = "Nekobin"
__HELP__ = """
──「 **Paste to Nekobin** 」──
-> `neko`
Create a Nekobin paste using replied to message.

"""

@app.on_message(Filters.user("self") & Filters.command(["neko"], Command))
async def paste(client, message):
    await message.edit_text("`Pasting...`")
    text = message.reply_to_message.text
    try:
        key = requests.post('https://nekobin.com/api/documents', json={"content": text}).json().get('result').get('key')
    except requests.exceptions.RequestException as e:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
    else:
        url = f'https://nekobin.com/{key}'
        reply_text = f'Parsed to **Nekobin** : {url}'
        await message.edit_text(
            reply_text,
            disable_web_page_preview=True,
        )