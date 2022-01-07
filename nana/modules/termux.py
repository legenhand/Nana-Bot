

import subprocess
from asyncio import sleep

from pyrogram import filters

from nana import Command, app, TERMUX_USER, AdminSettings, edrep

__MODULE__ = "Termux"
__HELP__ = """
For Termux API (You may need to host your Userbot on Termux):
And install Termux API from Playstore.

──「 **Battery Status** 」──
-> `bstats`
get yout phone's Battery Status.

──「 **Torch** 」──
-> `torch`
Turn your Device's Torch on & off   .

"""
torch = False

@app.on_message(filters.user(AdminSettings) & filters.command("bstats", Command))
async def bstat(_client, message):
    if TERMUX_USER:
        termux_command = subprocess.Popen("termux-battery-status", shell=True, stdout=subprocess.PIPE)
        my_bytes_value = termux_command.stdout.read()
        my_json = my_bytes_value.decode('utf8').replace("'", '').replace('"', '').replace("{", '').replace("}", '').replace(",", '').replace(" ", '').replace(":", ': ')
        await edrep(message, text=f"<b>Battery Status:</b>{my_json}")
    else:
        await edrep(message, text="This command is only for Termux users!")
        await sleep(2.0)
        await message.delete()


@app.on_message(filters.user(AdminSettings) & filters.command("torch", Command))
async def termux_torch(_client, message):
    global torch
    if torch:
        await edrep(message, text="Turning off torch...")
        await sleep(0.5)
        subprocess.Popen("termux-torch off", shell=True, stdout=subprocess.PIPE)
        torch = False
        await edrep(message, text="Torch turned off")
    else:
        await edrep(message, text="Turning on torch...")
        try:
            subprocess.Popen("termux-torch on", shell=True, stdout=subprocess.PIPE)
        except Exception as e:
            print(e)
            await edrep(message, text="Couldn't turn off torch!")
            await sleep(2.0)
            await message.delete()
            return
        torch = True
        await edrep(message, text="Torch turned on!")
    await sleep(2.0)
    await message.delete()