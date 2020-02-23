import os

from mega import Mega
from pyrogram import Filters

from nana import app, Command


@app.on_message(Filters.user("self") & Filters.command(["mega"], Command))
async def mega_download(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await message.edit("usage: mega (url)")
        return
    await message.edit("Processing...")
    if not os.path.exists('nana/downloads/mega'):
        os.makedirs('nana/downloads/mega')
    m = Mega()
    try:
        m.download_url(args[1], "nana/downloads/mega")
    except:
        await message.edit("Wrong Url or link not exist!")
    await message.edit("Success! file was downloaded at nana/downloads")


@app.on_message(Filters.user("self") & Filters.command(["megafile"], Command))
async def mega_downloaded_file(client, message):
    filelist = os.listdir("nana/downloads/mega")
    print(len(filelist))
    if len(filelist) == 0:
        await message.edit("You haven't download any files with mega! try to download something")
        return
    listoffile = "List of file you downloaded with mega: \n`"
    for i in range(len(filelist)):
        listoffile += filelist[i] + "\n"
    listoffile += "`"
    await message.edit(listoffile)
