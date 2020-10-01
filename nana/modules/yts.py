# With All rights Reserved
# Thanks to Userge and developers for this plugin
# https://github.com/UserGeTeam Give them a follow and a star

import asyncio
import os
import re
from urllib.parse import quote as urlencode

import aiohttp
import htmlement
import requests
from pyrogram import filters

from nana import app, Command, setbot, AdminSettings, edrep
from nana.helpers.aiohttp_helper import AioHttp

__MODULE__ = "YTS"
__HELP__ = """
This module is to send .torrent files using assistant.

──「 **YTS downloads** 」──
-> `yts`
Sends torrent file using assistant.
usage: `yts [Movie name]`
Example: `yts lion king`

──「 **Magnet Links** 」──
-> `ytsearch (movie name)`
Sends magnetlink using assistant.

──「 **Sakubei** 」──
-> `sb (anime name)`
return torrent link for anime or hentai.

"""


async def sukebei_search(query):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://sukebei.nyaa.si/?page=rss&c=0_0&f=0&q={urlencode(query)}') as resp:
            root = htmlement.fromstring(await resp.text())
    results = []
    for i in root.iterfind('.//channel/item'):
        title = i.find('title').text
        link = i.find('link').tail
        results.append((title, link))
    return results


@app.on_message(filters.user(AdminSettings) & filters.command("yts", Command))
async def yts(_client, message):
    qual = None
    max_limit = 5
    input_ = message.command[1]
    get_limit = re.compile(r'-l\d*[0-9]')
    get_quality = re.compile(r'-q\d*[PpDd]')
    _movie = re.sub(r'-\w*', "", input_).strip()
    if get_limit.search(input_) is None and get_quality.search(input_) is None:
        pass
    elif get_quality.search(input_) is not None and get_limit.search(input_) is not None:
        qual = get_quality.search(input_).group().strip('-q')
        max_limit = int(get_limit.search(input_).group().strip('-l'))
    elif get_quality.search(input_):
        qual = get_quality.search(input_).group().strip('-q')
    elif get_limit.search(input_):
        max_limit = int(get_limit.search(input_).group().strip('-l'))
    if len(input_) == 0:
        await edrep(message, text="No Input")
        await asyncio.sleep(3)
        await message.delete()
        return
    URL = "https://yts.mx/api/v2/list_movies.json?query_term={query}&limit={limit}"
    resp = requests.get(URL.format(query=_movie, limit=max_limit))
    datas = resp.json()
    if datas['status'] != "ok":
        await edrep(message, text="Wrong Status")
        await asyncio.sleep(3)
        await message.delete()
        return
    if datas['data']['movie_count'] == 0 or len(datas['data']) == 3:
        await edrep(message, text=f"{_movie} Not Found!")
        await asyncio.sleep(3)
        await message.delete()
        return
    _matches = datas['data']['movie_count']
    await edrep(message, text=f"`{_matches} Matches Found!, Asisstant sending {len(datas['data']['movies'])}.`")
    await asyncio.sleep(5)
    await message.delete()
    for data in datas['data']['movies']:
        _title = data['title_long']
        _rating = data['rating']
        _language = data['language']
        _torrents = data['torrents']
        def_quality = "1080p"
        _qualities = []
        for i in _torrents:
            _qualities.append(i['quality'])
        if qual in _qualities:
            def_quality = qual
        qualsize = [f"{j['quality']}: {j['size']}" for j in _torrents]
        capts = f'''
Title: {_title}
Rating: {_rating}
Language: {_language}
Size: {_torrents[_qualities.index(def_quality)]['size']}
Type: {_torrents[_qualities.index(def_quality)]['type']}
Seeds: {_torrents[_qualities.index(def_quality)]['seeds']}
Date Uploaded: {_torrents[_qualities.index(def_quality)]['date_uploaded']}
Available in: {qualsize}'''
        if def_quality in _qualities:
            files = f"{_title}{_torrents[_qualities.index(def_quality)]['quality']}.torrent"
            files = files.replace('/', '\\')
            with open(files, 'wb') as f:
                f.write(requests.get(_torrents[_qualities.index(def_quality)]['url']).content)
            await setbot.send_document(message.from_user.id,
            files,
            caption=capts
            )
            os.remove(files)
        else:
            await edrep(message, text="Not Found")
            return
    return


@app.on_message(filters.user(AdminSettings) & filters.command("ytsearch", Command))
async def yts_search(_client, message):
    cmd = message.command
    query = ""
    if len(cmd) > 1:
        query = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        query = message.reply_to_message.text
    elif len(cmd) == 1:
        await edrep(message, text="`No search query given for torrent search`")
        await asyncio.sleep(2)
        await message.delete()
        return
    rep = ""
    await edrep(message, text="`please check assistant for magnet urls`")
    count = 0
    try:
        torrents = await AioHttp().get_json(f"https://sjprojectsapi.herokuapp.com/torrent/?query={query}")
        for torrent in torrents:
            count += 1
            if count % 10 == 0:
                break
            title = torrent['name']
            size = torrent['size']
            seeders = torrent['seeder']
            leechers = torrent['leecher']
            magnet = torrent['magnet']
            try:
                rep = f"\n\n<b>{title}</b>\n"
                rep +=f"<b>Size:</b> {size}\n"
                rep +=f"<b>Seeders:</b> {seeders}\n"
                rep +=f"<b>Leechers:</b> {leechers}\n"
                rep +=f"<code>{magnet}</code>"
                await setbot.send_message(message.from_user.id, rep, parse_mode="html")
            except Exception as e:
                print(e)
        if rep == "":
            await edrep(message, text=f"No torrents found: __{query}__")
    except Exception as e:
        print(e)
        await edrep(message, text="API is Down!\nTry again later")
        await asyncio.sleep(2)
        await message.delete()
    await message.delete()


@app.on_message(filters.user(AdminSettings) & filters.command("sb", Command))
async def saku_bei(client, message):
    cmd = message.command
    query = ""
    if len(cmd) > 1:
        query = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        query = message.reply_to_message.text
    elif len(cmd) == 1:
        await edrep(message, text="`cant sakubei the void.`")
        await asyncio.sleep(2)
        await message.delete()
        return
    try:
        results = await sukebei_search(query)
    except Exception as e:
        print(e)
        await edrep(message, text="`something went wrong please check logs!")
        await asyncio.sleep(2)
        await message.delete()
    await edrep(message, text="`check assistant for magnet links`")
    await asyncio.sleep(7)
    await message.delete()
    count = 0
    for i, j in results:
        count += 1
        if count % 10 == 0:
            break
        rep = f'<b>Sakubei Torrent:</b>\n{i}: {j}'
        await setbot.send_message(message.from_user.id, rep)
    