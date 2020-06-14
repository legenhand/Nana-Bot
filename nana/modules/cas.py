
import requests
import asyncio

from pyrogram import Filters

from nana import app, Command
from nana.helpers.string import replace_text

__MODULE__ = "CAS Scanner"
__HELP__ = """
──「 **Combot Anti Spam Check** 」──
-> `cas` user_id

"""

@app.on_message(Filters.me & Filters.command(["cas"], Command))
async def cas(_client, message):
    cmd = message.command

    user = ""
    if len(cmd) > 1:
        user = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        user = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("`Usage: cas user_id`")
        await asyncio.sleep(2)
        await message.delete()
        return
    results = requests.get(f'https://api.cas.chat/check?user_id={user}').json()
    try:
        reply_text = f'`User ID: `{user}\n`Offenses: `{results["result"]["offenses"]}\n`Messages: `\n{results["result"]["messages"]}\n`Time Added: `{results["result"]["time_added"]}'
    except:
        reply_text = "`Record not found.`"
    await message.edit(replace_text(reply_text))