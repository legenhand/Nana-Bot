import os

from mega import Mega
from pyrogram import filters

from nana import app, Command, AdminSettings, edrep

__MODULE__ = "Mega"
__HELP__ = """
Download any file from URL or from telegram

──「 **Download mega file from URL** 」──
-> `mega (url)`
Give url as args to download it.

──「 **List Downloaded** 」──
-> `megafile`
List of file that have downloaded with mega.

"""


@app.on_message(filters.user(AdminSettings) & filters.command("mega", Command))
async def mega_download(_client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await edrep(message, text="usage: mega (url)")
        return
    await edrep(message, text="Processing...")
    if not os.path.exists('nana/downloads/mega'):
        os.makedirs('nana/downloads/mega')
    m = Mega()
    await m.download_url(message=message, url=args[1], dest_path="nana/downloads/mega")
    await edrep(message, text="Success! file was downloaded at nana/downloads")


@app.on_message(filters.user(AdminSettings) & filters.command("megafile", Command))
async def mega_downloaded_file(_client, message):
    filelist = os.listdir("nana/downloads/mega")
    print(len(filelist))
    if len(filelist) == 0:
        await edrep(message, text="You haven't download any files with mega! try to download something")
        return
    listoffile = "List of file you downloaded with mega: \n`"
    for item in filelist:
        listoffile += item + "\n"
    listoffile += "`"
    await edrep(message, text=listoffile)
