from requests import post
import shutil
import os
from nana import Command, app
from pyrogram import Filters
from time import sleep

CARBON_LANG = "Python"

@app.on_message(Filters.user("self") & Filters.command(["carbon"], Command))
async def carbon_api(client, message):
    json = {
        "backgroundColor": "rgba(144, 19, 254, 100)",
        "theme": "dracula"
    }
    if message.reply_to_message:
        r = message.reply_to_message
        json["code"] = r.text
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
        await client.send_photo(message.chat.id, filename)
        await message.delete()
    else:
        await message.edit('Image Couldn\'t be retreived')
        await message.delete()
    os.remove(filename)

@app.on_message(Filters.user("self") & Filters.command(["carbonlang"], Command))
async def carbon_lang(client, message):
    global CARBON_LANG
    cmd = message.command

    type_text = ""
    if len(cmd) > 1:
        type_text = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        type_text = message.reply_to_message.text
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit("Give me something to carbonize")
        await sleep(2)
        await message.delete()
        return

def get_carbon_lang():
    # Gets carbon language. Default py
    return CARBON_LANG