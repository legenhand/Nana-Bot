

from pyrogram import Filters
import json
from asyncio import sleep
import subprocess

from nana import Command, app, TERMUX_USER

__MODULE__ = "Termux"
__HELP__ = """
For Termux API (You may need to host your Userbot on Termux):
And install Termux API from Playstore.

──「 **Battery Status** 」──
-> `bstats`
get yout phone's Battery Status.

"""

@app.on_message(Filters.me & Filters.command(["bstats"], Command))
async def bstat(_client, message):
    if TERMUX_USER:
        termux_command = subprocess.Popen("termux-battery-status", shell=True, stdout=subprocess.PIPE)
        my_bytes_value = termux_command.stdout.read()
        my_json = my_bytes_value.decode('utf8').replace("'", '').replace('"', '').replace("{", '').replace("}", '').replace(",", '').replace(" ", '')
        await message.edit(f"<b>Battery Status:</b>{my_json}")
    else:
        await message.edit("This command is only for Termux users!")
        await sleep(2.0)
        await message.delete()