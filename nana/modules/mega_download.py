# Copyright (C) 2020 Adek Maulana.
# All rights reserved.
#

import json
import os
import re
import time
from os.path import exists
from subprocess import PIPE, Popen
from urllib.error import HTTPError

from pySmartDL import SmartDL
from pyrogram import filters

from nana import app, Command, AdminSettings, edrep
from .downloads import humanbytes


async def subprocess_run(cmd, message):
    subproc = Popen(cmd, stdout=PIPE, stderr=PIPE,
                    shell=True, universal_newlines=True,
                    executable="bash")
    talk = subproc.communicate()
    exit_code = subproc.returncode
    if exit_code != 0:
        await edrep(message, text=
            '```An error was detected while running the subprocess:\n'
            f'exit code: {exit_code}\n'
            f'stdout: {talk[0]}\n'
            f'stderr: {talk[1]}```')
        return exit_code
    return talk


@app.on_message(filters.user(AdminSettings) & filters.command("megadownload", Command))
async def mega_downloader(_client, message):
    args = message.text.split(None, 1)
    await edrep(message, text="`Processing...`")
    msg_link = await message.reply_to_message.text
    link = args[1]
    if link:
        pass
    elif msg_link:
        link = msg_link.text
    else:
        await edrep(message, text="Usage: `mega <mega url>`")
        return
    try:
        link = re.findall(r'\bhttps?://.*mega.*\.nz\S+', link)[0]
    except IndexError:
        await edrep(message, text="`No MEGA.nz link found`\n")
        return
    cmd = f'bin/megadown -q -m {link}'
    result = await subprocess_run(cmd, message)
    try:
        data = json.loads(result[0])
    except json.JSONDecodeError:
        await edrep(message, text="`Error: Can't extract the link`\n")
        return
    except TypeError:
        return
    except IndexError:
        return
    file_name = data["file_name"]
    file_url = data["url"]
    hex_key = data["hex_key"]
    hex_raw_key = data["hex_raw_key"]
    temp_file_name = file_name + ".temp"
    downloaded_file_name = "./" + "" + temp_file_name
    downloader = SmartDL(
        file_url, downloaded_file_name, progress_bar=False)
    display_message = None
    try:
        downloader.start(blocking=False)
    except HTTPError as e:
        await edrep(message, text="`" + str(e) + "`")
        return
    while not downloader.isFinished():
        status = downloader.get_status().capitalize()
        total_length = downloader.filesize if downloader.filesize else None
        downloaded = downloader.get_dl_size()
        percentage = int(downloader.get_progress() * 100)
        progress = downloader.get_progress_bar()
        speed = downloader.get_speed(human=True)
        estimated_total_time = downloader.get_eta(human=True)
        try:
            current_message = (
                f"**{status}**..."
                f"\nFile Name: `{file_name}`\n"
                f"\n{progress} `{percentage}%`"
                f"\n{humanbytes(downloaded)} of {humanbytes(total_length)}"
                f" @ {speed}"
                f"\nETA: {estimated_total_time}"
            )
            if status == "Downloading":
                await edrep(message, text=current_message)
                time.sleep(0.2)
            elif status == "Combining":
                if display_message != current_message:
                    await edrep(message, text=current_message)
                    display_message = current_message
        except Exception as e:
            print(e)
            pass
    if downloader.isSuccessful():
        download_time = downloader.get_dl_time(human=True)
        if exists(temp_file_name):
            await decrypt_file(
                file_name, temp_file_name, hex_key, hex_raw_key, message)
            await edrep(message, text=f"`{file_name}`\n\n"
                              "Successfully downloaded\n"
                              f"Download took: {download_time}")
    else:
        await edrep(message, text="Failed to download, check heroku Log for details")
        for e in downloader.get_errors():
            await edrep(message, text=str(e))
    return


async def decrypt_file(file_name, temp_file_name,
                       hex_key, hex_raw_key, message):
    await edrep(message, text="Decrypting file...")
    cmd = ("cat '{}' | openssl enc -d -aes-128-ctr -K {} -iv {} > '{}'"
           .format(temp_file_name, hex_key, hex_raw_key, file_name))
    await subprocess_run(cmd, message)
    os.remove(temp_file_name)
    return
