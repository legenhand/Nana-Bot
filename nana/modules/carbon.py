from requests import post
import shutil
import os
from nana import Command, app
from pyrogram import Filters
from time import sleep
from nana.helpers.PyroHelpers import ReplyCheck

CARBON_LANG = "Auto"

@app.on_message(Filters.user("self") & Filters.command(["carbon"], Command))
async def carbon_api(client, message):
    json = {
        "backgroundColor": "rgba(0, 255, 230, 100)",
        "theme": "VSCode"
    }
    if message.reply_to_message:
        r = message.reply_to_message
        json["code"] = r.text
        await message.edit_text("Carbonizing code...")
    else:
        await message.edit("Usage: `carbon` (reply to a code or text)")
    json["language"] = CARBON_LANG
    apiUrl = "http://carbonnowsh.herokuapp.com"
    r = post(apiUrl,json=json,stream=True)
    filename = 'carbon.jpg'
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        await client.send_photo(message.chat.id, filename, reply_to_message_id=ReplyCheck(message))
        await message.delete()
    else:
        await message.edit('Image Couldn\'t be retreived')
        await message.delete()
    os.remove(filename)