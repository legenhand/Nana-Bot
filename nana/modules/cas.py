
import requests
from time import sleep

from pyrogram import Filters, Message, User
from pyrogram.api import functions
from pyrogram.errors import PeerIdInvalid

from nana import app, Command
from nana.helpers.PyroHelpers import ReplyCheck

__MODULE__ = "CAS Scanner"
__HELP__ = """
──「 **Combot Anti Spam Check** 」──
-> `cas` @username
-> `cas` (reply to a text) To find information about a person.

"""

def replace_text(text):
        return text.replace("[", "").replace("]", "").replace("\"", "").replace("\\r", "").replace("\\n", "\n").replace(
            "\\", "")

@app.on_message(Filters.me & Filters.command(["cas"], Command))
async def cas(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif message.reply_to_message and len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.edit("I don't know that User.")
        sleep(2)
        await message.delete()
        return
    results = requests.get(f'https://api.cas.chat/check?user_id={user}').json()
    try:
        reply_text = f'`User ID: `{user}\n`Offenses: `{results["result"]["offenses"]}\n`Messages: `\n{results["result"]["messages"]}\n`Time Added: `{results["result"]["time_added"]}'
    except:
        reply_text = "`Record not found.`"
    await message.edit(replace_text(reply_text), reply_to_message_id=ReplyCheck(message))