import os
from asyncio import sleep

from pyrogram import Filters

from nana import Command, app

CARBON_LANG = "py"

def get_carbon_lang():
    return CARBON_LANG

@app.on_message(Filters.user("self") & Filters.command(["carbon"], Command))
async def carbon(client, message):
    carbon_text = message.text[8:]
    # Write the code to a file cause carbon-now-cli wants a file.
    file = "nana/downloads/carbon.{}".format(get_carbon_lang())
    f = open(file, "w+")
    f.write(carbon_text)
    f.close()

    await message.edit_text("Carbonizing code...")
    # Do the thing
    os.system("carbon-now -h -t nana/downloads/carbon {}".format(file))
    # await message.edit_text("Carbonizing completed...")
    # Send the thing
    await client.send_photo(message.chat.id, 'nana/downloads/carbon.png')
    await message.delete()

@app.on_message(Filters.user("self") & Filters.command(["carbonlang"], Command))
async def carbonlang(client, message):
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
    CARBON_LANG = type_text
    await message.edit_text("Carbon type set to {}".format(type_text))
    await sleep(2)
    await message.delete()