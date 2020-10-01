
import asyncio
import os
import shlex
from datetime import datetime
from os.path import basename
from typing import Tuple, Optional

import requests
import tracemoepy
from bs4 import BeautifulSoup
from pyrogram import filters

from nana import app, Command, logging, AdminSettings, edrep
from nana.helpers.PyroHelpers import ReplyCheck

__MODULE__ = "Reverse"
__HELP__ = """
This module will help you Reverse Search Media

──「 **Google Reverse Search** 」──
-> `reverse (reply to a media)`
Reverse search any supported media by google

──「 **TraceMoe Reverse Search** 」──
-> `areverse (reply to a media)`
Anime reverse search any supported media by tracemoe

"""

screen_shot = "nana/downloads/"

_LOG = logging.getLogger(__name__)


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal."""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(*args,
                                                   stdout=asyncio.subprocess.PIPE,
                                                   stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return (stdout.decode('utf-8', 'replace').strip(),
            stderr.decode('utf-8', 'replace').strip(),
            process.returncode,
            process.pid)


async def take_screen_shot(video_file: str, duration: int, path: str = '') -> Optional[str]:
    """take a screenshot."""
    ttl = duration // 2
    thumb_image_path = path or os.path.join(screen_shot, f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await run_cmd(command))[1]
    if err:
        _LOG.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


@app.on_message(filters.user(AdminSettings) & filters.command("reverse", Command))
async def google_rs(client, message):
    start = datetime.now()
    dis_loc = ''
    out_str = "`Reply to an image`"
    if message.reply_to_message:
        message_ = message.reply_to_message
        if message_.sticker and message_.sticker.file_name.endswith('.tgs'):
            await message.delete()
            return
        if message_.photo or message_.animation or message_.sticker:
            dis = await client.download_media(
                message=message_,
                file_name=screen_shot
            )
            dis_loc = os.path.join(screen_shot, os.path.basename(dis))
        if message_.animation or message_.video:
            await edrep(message, text="`Converting this Gif`")
            img_file = os.path.join(screen_shot, "grs.jpg")
            await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await edrep(message, text="`Something went wrong in Conversion`")
                await asyncio.sleep(5)
                await message.delete()
                return
            dis_loc = img_file
        base_url = "http://www.google.com"
        if dis_loc:
            search_url = "{}/searchbyimage/upload".format(base_url)
            multipart = {
                "encoded_image": (dis_loc, open(dis_loc, "rb")),
                "image_content": ""
            }
            google_rs_response = requests.post(search_url, files=multipart, allow_redirects=False)
            the_location = google_rs_response.headers.get("Location")
            os.remove(dis_loc)
        else:
            await message.delete()
            return
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = base_url + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        end = datetime.now()
        ms = (end - start).seconds
        out_str = f"""<b>Time Taken</b>: {ms} seconds
<b>Possible Related Search</b>: <a href="{prs_url}">{prs_text}</a>
<b>More Info</b>: Open this <a href="{the_location}">Link</a>
"""
    await edrep(message, text=out_str, parse_mode="HTML", disable_web_page_preview=True)


@app.on_message(filters.user(AdminSettings) & filters.command("areverse", Command))
async def tracemoe_rs(client, message):
    dis_loc = ''
    if message.reply_to_message:
        message_ = message.reply_to_message
        if message_.sticker and message_.sticker.file_name.endswith('.tgs'):
            await message.delete()
            return
        if message_.photo or message_.animation or message_.sticker:
            dis = await client.download_media(
                message=message_,
                file_name=screen_shot
            )
            dis_loc = os.path.join(screen_shot, os.path.basename(dis))
        if message_.animation:
            await edrep(message, text="`Converting this Gif`")
            img_file = os.path.join(screen_shot, "grs.jpg")
            await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await edrep(message, text="`Something went wrong in Conversion`")
                await asyncio.sleep(5)
                await message.delete()
                return
            dis_loc = img_file
        if message_.video:
            nama = "video_{}-{}.mp4".format(message.reply_to_message.video.date, message.reply_to_message.video.file_size)
            await client.download_media(message.reply_to_message.video, file_name="nana/downloads/" + nama)
            dis_loc = "nana/downloads/" + nama
            img_file = os.path.join(screen_shot, "grs.jpg")
            await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await edrep(message, text="`Something went wrong in Conversion`")
                await asyncio.sleep(5)
                await message.delete()
                return
        if dis_loc:
            tracemoe = tracemoepy.async_trace.Async_Trace()
            if message_.video:
                search = await tracemoe.search(img_file, encode=True)
                os.remove(img_file)
            else:
                search = await tracemoe.search(dis_loc, encode=True)
            os.remove(dis_loc)
            result = search['docs'][0]
            ms_g = f"**Title**: {result['title_english']}" \
                  f"\n**Similarity**: {result['similarity']*100}"\
                  f"\n**Episode**: {result['episode']}"
            preview = await tracemoe.video_preview(search)
            with open('preview.mp4', 'wb') as f:
                f.write(preview)
            await message.delete()
            await client.send_video(message.chat.id,
                                    'preview.mp4',
                                    caption=ms_g,
                                    reply_to_message_id=ReplyCheck(message)
                                    )
            await asyncio.sleep(5)
            await message.delete()
            os.remove('preview.mp4')
        else:
            await message.delete()
            return
    else:
        await edrep(message, text="`Reply to a message to proceed`")
        await asyncio.sleep(5)
        await message.delete()
        return
