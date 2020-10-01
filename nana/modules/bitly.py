from asyncio import sleep

from pyrogram import filters

from nana import app, Command, AdminSettings, edrep
from nana.helpers.expand import expand_url

__MODULE__ = "Link Expander"
__HELP__ = """
This module will expand your link

──「 **expand url** 」──
-> `expand (link)`
Reply or parse arg of url to expand
"""


@app.on_message(filters.command("expand", Command) & filters.user(AdminSettings))
async def expand(_client, message):
    if message.reply_to_message:
        url = message.reply_to_message.text or message.reply_to_message.caption
    elif len(message.command) > 1:
        url = message.command[1]
    else:
        url = None

    if url:
        expanded = await expand_url(url)
        if expanded:
            await edrep(message, text=f"<b>Shortened URL</b>: {url}\n<b>Expanded URL</b>: {expanded}", disable_web_page_preview=True)
            return
        else:
            await edrep(message, text="`i Cant expand this url :p`")
            await sleep(3)
            await message.delete()
    else:
        await edrep(message, text="Nothing to expand")
