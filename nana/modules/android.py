from asyncio import sleep

import requests
from pyrogram import filters

from nana import app, Command

__MODULE__ = "Device"
__HELP__ = """
Take a picture of website. You can select one for use this.

──「 **Device** 」──
-> `device (codename)`

Usage: `device (codename)`

"""

DEVICE_LIST = "https://raw.githubusercontent.com/androidtrackers/certified-android-devices/master/by_device.json"


@app.on_message(filters.me & filters.command(["device"], Command))
async def get_device(_client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `device (codename)`")
        return
    getlist = requests.get(DEVICE_LIST).json()
    target_device = message.text.split()[1].lower()
    if target_device in list(getlist):
        device = getlist.get(target_device)
        text = ""
        for x in device:
            text += f"Brand: `{x['brand']}`\nName: `{x['name']}`\nDevice: `{x['model']}`\nCodename: `{target_device}`"
            text += "\n\n"
        await message.edit(text)
    else:
        await message.edit(f"Device {target_device} was not found!")
        await sleep(5)
        await message.delete()
