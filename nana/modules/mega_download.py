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
from pyrogram import Filters

from nana import app, Command
from .downloads import humanbytes


async def subprocess_run(cmd, megadl):
    subproc = Popen(cmd, stdout=PIPE, stderr=PIPE,
                    shell=True, universal_newlines=True,
                    executable="bash")
    talk = subproc.communicate()
    exit_code = subproc.returncode
    if exit_code != 0:
        await megadl.edit(
            '```An error was detected while running the subprocess:\n'
            f'exit code: {exit_code}\n'
            f'stdout: {talk[0]}\n'
            f'stderr: {talk[1]}```')
        return exit_code
    return talk


@app.on_message(Filters.me & Filters.command(["megadownload"], Command))
async def mega_downloader(_client, megadl):
    args = megadl.text.split(None, 1)
    await megadl.edit("`Processing...`")
    msg_link = await megadl.reply_to_message.text
    link = args[1]
    if link:
        pass
    elif msg_link:
        link = msg_link.text
    else:
        await megadl.edit("Usage: `.mega <mega url>`")
        return
    try:
        link = re.findall(r'\bhttps?://.*mega.*\.nz\S+', link)[0]
    except IndexError:
        await megadl.edit("`No MEGA.nz link found`\n")
        return
    cmd = f'bin/megadown -q -m {link}'
    result = await subprocess_run(cmd, megadl)
    try:
        data = json.loads(result[0])
    except json.JSONDecodeError:
        await megadl.edit("`Error: Can't extract the link`\n")
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
        await megadl.edit("`" + str(e) + "`")
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
                await megadl.edit(current_message)
                time.sleep(0.2)
            elif status == "Combining":
                if display_message != current_message:
                    await megadl.edit(current_message)
                    display_message = current_message
        except Exception:
            pass
    if downloader.isSuccessful():
        download_time = downloader.get_dl_time(human=True)
        if exists(temp_file_name):
            await decrypt_file(
                file_name, temp_file_name, hex_key, hex_raw_key, megadl)
            await megadl.edit(f"`{file_name}`\n\n"
                              "Successfully downloaded\n"
                              f"Download took: {download_time}")
    else:
        await megadl.edit("Failed to download, check heroku Log for details")
        for e in downloader.get_errors():
            megadl.edit(str(e))
    return


async def decrypt_file(file_name, temp_file_name,
                       hex_key, hex_raw_key, megadl):
    await megadl.edit("Decrypting file...")
    cmd = ("cat '{}' | openssl enc -d -aes-128-ctr -K {} -iv {} > '{}'"
           .format(temp_file_name, hex_key, hex_raw_key, file_name))
    await subprocess_run(cmd, megadl)
    os.remove(temp_file_name)
    return
