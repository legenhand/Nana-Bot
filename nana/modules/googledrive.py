import asyncio
import os
import time

import requests
from bs4 import BeautifulSoup
from pydrive.drive import GoogleDrive
from pyrogram import Filters

from nana import app, setbot, Command, gauth, gdrive_credentials, HEROKU_API
from nana.helpers.parser import cleanhtml
from nana.modules.downloads import download_url
from .downloads import progressdl

__MODULE__ = "Google Drive"
__HELP__ = """
Google Drive stuff, for login just type /gdrive in Assistant bot

──「 **Download From Drive URL** 」──
-> `gdrive download (url)`
Give url as args to download it.

──「 **Upload From local to Google Drive** 」──
-> `gdrive upload (file)`
Upload from local storage to gdrive

──「 **Mirror and save to GDrive file** 」──
-> `gdrive mirror`
This can mirror from file download was limited, but not for deleted file

──「 **Mirror from telegram to GDrive** 」──
-> `gdrive tgmirror`
Download file from telegram, and mirror it to Google Drive

──「 **Mirror from URL to GDrive** 」──
-> `gdrive urlmirror`
Download file from URL, and mirror it to Google Drive
"""


async def get_drivedir(drive):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for drivefolders in file_list:
        if drivefolders['title'] == 'Nana Drive':
            return drivefolders['id']
    mkdir = drive.CreateFile({'title': 'Nana Drive', "mimeType": "application/vnd.google-apps.folder"})
    mkdir.Upload()


async def get_driveid(driveid):
    if "http" in driveid or "https" in driveid:
        drivesplit = driveid.split('drive.google.com')[1]
        if '/d/' in drivesplit:
            driveid = drivesplit.split('/d/')[1].split('/')[0]
        elif 'id=' in drivesplit:
            driveid = drivesplit.split('id=')[1].split('&')[0]
        else:
            return False
    return driveid


async def get_driveinfo(driveid):
    getdrivename = BeautifulSoup(
        requests.get('https://drive.google.com/file/d/{}/view'.format(driveid), allow_redirects=False).content)
    filename = cleanhtml(str(getdrivename.find('title'))).split(" - ")[0]
    return filename


@app.on_message(Filters.me & Filters.command(["credentials"], Command))
async def credentials(_client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await message.edit("Write any args here!")
        return
    if len(args) == 2:
        file = open("client_secrets.json", "w")
        file.write(args[1])
        file.close()
        await message.edit("credentials success saved on client_secrets")
        return


@app.on_message(Filters.me & Filters.command(["gdrive"], Command))
async def gdrive_stuff(client, message):
    gauth.LoadCredentialsFile("nana/session/drive")
    if gauth.credentials is None:
        if HEROKU_API:
            if gdrive_credentials:
                file = open("client_secrets.json", "w")
                file.write(gdrive_credentials)
                file.close()
        await message.edit(
            "You are not logged in to your google drive account!\nYour assistant bot may help you to login google "
            "drive, check your assistant bot for more information!")
        gdriveclient = os.path.isfile("client_secrets.json")
        if not gdriveclient:
            await setbot.send_message(message.from_user.id,
                                      "Hello, look like you're not logged in to google drive 🙂\nI can help you to "
                                      "login.\n\nFirst of all, you need to activate your google drive API\n1. [Go "
                                      "here](https://developers.google.com/drive/api/v3/quickstart/python), "
                                      "click **Enable the drive API**\n2. Login to your google account (skip this if "
                                      "you're already logged in)\n3. After logged in, click **Enable the drive API** "
                                      "again, and click **Download Client Configuration** button, download that.\n4. "
                                      "After downloaded that file, open that file then copy all of that content, "
                                      "back to telegram then do .credentials (copy the content of that file)  do "
                                      "without bracket\n\nAfter that, you can go next guide by type /gdrive")
        else:
            try:
                gauth.GetAuthUrl()
            except:
                await setbot.send_message(message.from_user.id,
                                          "Wrong Credentials! Check var ENV gdrive_credentials on heroku or do "
                                          ".credentials (your credentials) for change your Credentials")
                return
            await setbot.send_message(message.from_user.id,
                                      "Hello, look like you're not logged in to google drive :)\nI can help you to "
                                      "login.\n\n**To login Google Drive**\n1. `/gdrive` to get login URL\n2. After "
                                      "you're logged in, copy your Token.\n3. `/gdrive (token)` without `(` or `)` to "
                                      "login, and your session will saved to `nana/session/drive`.\n\nDon't share your "
                                      "session to someone, else they will hack your google drive account!")
        return
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()

    drive = GoogleDrive(gauth)
    drive_dir = await get_drivedir(drive)

    if len(message.text.split()) == 3 and message.text.split()[1] == "download":
        await message.edit("Downloading...")
        driveid = await get_driveid(message.text.split()[2])
        if not driveid:
            await message.edit(
                "Invaild URL!\nIf you think this is bug, please go to your Assistant bot and type `/reportbug`")
            return
        filename = await get_driveinfo(driveid)
        if not filename:
            await message.edit(
                "Invaild URL!\nIf you think this is bug, please go to your Assistant bot and type `/reportbug`")
            return
        await message.edit("Downloading for `{}`\nPlease wait...".format(filename))
        download = drive.CreateFile({'id': driveid})
        download.GetContentFile(filename)
        try:
            os.rename(filename, "nana/downloads/" + filename)
        except FileExistsError:
            os.rename(filename, "nana/downloads/" + filename + ".2")
        await message.edit("Downloaded!\nFile saved to `{}`".format("nana/downloads/" + filename))
    elif len(message.text.split()) == 3 and message.text.split()[1] == "upload":
        filerealname = message.text.split()[2].split(None, 1)[0]
        filename = "nana/downloads/{}".format(filerealname)
        checkfile = os.path.isfile(filename)
        if not checkfile:
            await message.edit("File `{}` was not found!".format(filerealname))
            return
        await message.edit("Uploading `{}`...".format(filerealname))
        upload = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": drive_dir}], 'title': filerealname})
        upload.SetContentFile(filename)
        upload.Upload()
        upload.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
        await message.edit(
            "Uploaded!\nDownload link: [{}]({})\nDirect download link: [{}]({})".format(filerealname, upload[
                'alternateLink'], filerealname, upload['downloadUrl']))
    elif len(message.text.split()) == 3 and message.text.split()[1] == "mirror":
        message.edit("Mirroring...")
        driveid = await get_driveid(message.text.split()[2])
        if not driveid:
            await message.edit(
                "Invaild URL!\nIf you think this is bug, please go to your Assistant bot and type `/reportbug`")
            return
        filename = await get_driveinfo(driveid)
        if not filename:
            await message.edit(
                "Invaild URL!\nIf you think this is bug, please go to your Assistant bot and type `/reportbug`")
            return
        mirror = drive.auth.service.files().copy(fileId=driveid,
                                                 body={"parents": [{"kind": "drive#fileLink", "id": drive_dir}],
                                                       'title': filename}).execute()
        new_permission = {'type': 'anyone', 'value': 'anyone', 'role': 'reader'}
        drive.auth.service.permissions().insert(fileId=mirror['id'], body=new_permission).execute()
        await message.edit(
            "Done!\nDownload link: [{}]({})\nDirect download link: [{}]({})".format(filename, mirror['alternateLink'],
                                                                                    filename, mirror['downloadUrl']))
    elif len(message.text.split()) == 2 and message.text.split()[1] == "tgmirror":
        if message.reply_to_message:
            await message.edit("__Downloading...__")
            c_time = time.time()
            if message.reply_to_message.photo:
                nama = "photo_{}_{}.png".format(message.reply_to_message.photo, message.reply_to_message.photo.date)
                await client.download_media(message.reply_to_message.photo, file_name="nana/downloads/" + nama,
                                            progress=lambda d, t: asyncio.get_event_loop().create_task(
                                                progressdl(d, t, message, c_time, "Downloading...")))
            elif message.reply_to_message.animation:
                nama = "giphy_{}-{}.gif".format(message.reply_to_message.animation.date,
                                                message.reply_to_message.animation.file_size)
                await client.download_media(message.reply_to_message.animation, file_name="nana/downloads/" + nama,
                                            progress=lambda d, t: asyncio.get_event_loop().create_task(
                                                progressdl(d, t, message, c_time, "Downloading...")))
            elif message.reply_to_message.video:
                nama = "video_{}-{}.mp4".format(message.reply_to_message.video.date,
                                                message.reply_to_message.video.file_size)
                await client.download_media(message.reply_to_message.video, file_name="nana/downloads/" + nama,
                                            progress=lambda d, t: asyncio.get_event_loop().create_task(
                                                progressdl(d, t, message, c_time, "Downloading...")))
            elif message.reply_to_message.sticker:
                nama = "sticker_{}_{}.webp".format(message.reply_to_message.sticker.date,
                                                   message.reply_to_message.sticker.set_name)
                await client.download_media(message.reply_to_message.sticker, file_name="nana/downloads/" + nama,
                                            progress=lambda d, t: asyncio.get_event_loop().create_task(
                                                progressdl(d, t, message, c_time, "Downloading...")))
            elif message.reply_to_message.audio:
                nama = "{}".format(message.reply_to_message.audio.file_name)
                await client.download_media(message.reply_to_message.audio, file_name="nana/downloads/" + nama,
                                            progress=lambda d, t: asyncio.get_event_loop().create_task(
                                                progressdl(d, t, message, c_time, "Downloading...")))
            elif message.reply_to_message.voice:
                nama = "audio_{}.ogg".format(message.reply_to_message.voice)
                await client.download_media(message.reply_to_message.voice, file_name="nana/downloads/" + nama,
                                            progress=lambda d, t: asyncio.get_event_loop().create_task(
                                                progressdl(d, t, message, c_time, "Downloading...")))
            elif message.reply_to_message.document:
                nama = "{}".format(message.reply_to_message.document.file_name)
                await client.download_media(message.reply_to_message.document, file_name="nana/downloads/" + nama,
                                            progress=lambda d, t: asyncio.get_event_loop().create_task(
                                                progressdl(d, t, message, c_time, "Downloading...")))
            else:
                await message.edit("Unknown file!")
                return
            upload = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": drive_dir}], 'title': nama})
            upload.SetContentFile("nana/downloads/" + nama)
            upload.Upload()
            upload.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
            await message.edit(
                "Done!\nDownload link: [{}]({})\nDirect download link: [{}]({})".format(nama, upload['alternateLink'],
                                                                                        nama, upload['downloadUrl']))
            os.remove("nana/downloads/" + nama)
        else:
            await message.edit("Reply document to mirror it to gdrive")
    elif len(message.text.split()) == 3 and message.text.split()[1] == "urlmirror":
        await message.edit("Downloading...")
        URL = message.text.split()[2]
        nama = URL.split("/")[-1]
        time_dl = await download_url(URL, nama)
        if "Downloaded" not in time_dl:
            await message.edit("Failed to download file, invaild url!")
            return
        await message.edit(f"Downloaded with {time_dl}.\nNow uploading...")
        upload = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": drive_dir}], 'title': nama})
        upload.SetContentFile("nana/downloads/" + nama)
        upload.Upload()
        upload.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
        await message.edit(
            "Done!\nDownload link: [{}]({})\nDirect download link: [{}]({})".format(nama, upload['alternateLink'], nama,
                                                                                    upload['downloadUrl']))
        os.remove("nana/downloads/" + nama)
    else:
        await message.edit(
            "Usage:\n-> `gdrive download <url/gid>`\n-> `gdrive upload <file>`\n-> `gdrive mirror <url/gid>`\n\nFor "
            "more information about this, go to your assistant.")
