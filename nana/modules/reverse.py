# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.
# Ported to Nana by @pokurt

import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from pyrogram import Filters

from nana import app, Command

__MODULE__ = "Reverse Search"
__HELP__ = """
This module will help you Reverse Ssearch Media from Google

──「 **Google Reverse Search** 」──
-> `reverse (reply to a media)`
Reverse search any supported media by google with this command

`Copyright (C) 2020 by UsergeTeam@Github,`
`Ported to Nana - Userbot by` @pokurt

"""

@app.on_message(Filters.me & Filters.command(["reverse"], Command))
async def bitly(client, message):
    start = datetime.now()
    dis_loc = ''
    base_url = "http://www.google.com"
    out_str = "Reply to an image to do Google Reverse Search"
    if message.reply_to_message:
        message_ = message.reply_to_message
        if message_.sticker and message_.sticker.file_name.endswith('.tgs'):
            await message.edit('Reverse search for Animated stickers are yet not implemented')
            return
        if message_.photo or message_.animation or message_.sticker:
            dis = await client.download_media(message=message_, file_name="/root/nana/")
            dis_loc = os.path.join("/root/nana/", os.path.basename(dis))
        if message_.animation:
            await message.edit("Converting this Gif to Image")
            img_file = os.path.join("/root/nana/", "grs.jpg")
            # await take_screen_shot(dis_loc, 0, img_file)
            if not os.path.lexists(img_file):
                await message.edit("Something went wrong in Conversion")
            dis_loc = img_file
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
            await message.edit("No Results will pass")
        await message.edit("Found Google Result.")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        }
        response = requests.get(the_location, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        prs_div = soup.find_all("div", {"class": "r5a77d"})[0]
        prs_anchor_element = prs_div.find("a")
        prs_url = base_url + prs_anchor_element.get("href")
        prs_text = prs_anchor_element.text
        soup.find(id="jHnbRc")
        # img_size = img_size_div.find_all("div")
        end = datetime.now()
        ms = (end - start).seconds
        out_str = f"""
    <b>Possible Related Search</b>: <a href="{prs_url}">{prs_text}</a>
    <b>More Info</b>: Open this <a href="{the_location}">Link</a>
    <b>Time Taken</b>: {ms} seconds"""
    await message.edit(out_str, parse_mode="HTML", disable_web_page_preview=True)