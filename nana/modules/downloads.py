import asyncio
import json
import logging
import math
import os
import re
import time
import urllib.parse
from random import choice

import requests
from bs4 import BeautifulSoup
from pyDownload import Downloader
from pyrogram import filters

from nana import app, Command, AdminSettings, edrep

__MODULE__ = "Downloads"
__HELP__ = """
Download any file from URL or from telegram

──「 **Download From URL** 」──
-> `dl (url)`
Give url as args to download it.

──「 **Download From Telegram** 」──
-> `download`
Reply a document to download it.

──「 **Upload To Telegram** 」──
-> `upload (path)`
give path of file to send to telegram.

──「 **List files and directories** 」──
-> `ls (path)`
see list of files and directories, path is optional

──「 **Direct Link Download** 」──
-> `direct (url)`
Create A direct link download

Supported Link
`gdrive     | zippyshare   | mega
yadi.sk    | mediafire    | osdn.net
github.com | Sourceforge
androidfilehost.com`
"""


@app.on_message(filters.user(AdminSettings) & filters.command("ls", Command))
async def ls(_client, message):
    args = message.text.split(None, 1)
    basepath = "nana/{}".format(args[1]) if len(args) == 2 else "nana/"
    directory = ""
    listfile = ""
    for entry in os.listdir(basepath):
        if os.path.isdir(os.path.join(basepath, entry)):
            directory += "\n{}".format(entry)
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            listfile += "\n{}".format(entry)
    await edrep(message, text="**List directory :**`{}`\n**List file :**`{}`".format(directory, listfile))


@app.on_message(filters.user(AdminSettings) & filters.command("upload", Command))
async def upload_file(client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        await edrep(message, text="usage : upload (path)")
        return
    path = "nana/{}".format(args[1])
    try:
        await app.send_document(message.chat.id, path, progress=lambda d, t: asyncio.get_event_loop().create_task(
            progressdl(d, t, message, time.time(), "Uploading...")))
    except Exception as e:
        logging.error("Exception occured", exc_info=True)
        logging.error(e)
        await edrep(message, text="`File not found!`")
        return
    await edrep(message, text="`Success!`")
    await asyncio.sleep(5)
    await client.delete_messages(message.chat.id, message.message_id)


async def time_parser(start, end):
    time_end = end - start
    month = time_end // 2678400
    days = time_end // 86400
    hours = time_end // 3600 % 24
    minutes = time_end // 60 % 60
    seconds = time_end % 60

    times = ""
    if month:
        times += "{} month, ".format(month)
    if days:
        times += "{} days, ".format(days)
    if hours:
        times += "{} hours, ".format(hours)
    if minutes:
        times += "{} minutes, ".format(minutes)
    if seconds:
        times += "{} seconds".format(seconds)
    if times == "":
        times = "{} miliseconds".format(time_end)

    return times


async def download_url(url, file_name):
    start = int(time.time())
    downloader = Downloader(url=url)
    end = int(time.time())
    times = await time_parser(start, end)
    downlaoded = f"⬇️ Downloaded `{file_name}` in {times}"
    downlaoded += "\n🗂 File name: {}".format(file_name)
    size = os.path.getsize(downloader.file_name)
    if size > 1024000000:
        file_size = round(size / 1024000000, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " GB`\n"
    elif 1024000 < size < 1024000000:
        file_size = round(size / 1024000, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " MB`\n"
    elif 1024 < size < 1024000:
        file_size = round(size / 1024, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " KB`\n"
    elif size < 1024:
        file_size = round(size, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " Byte`\n"

    try:
        os.rename(downloader.file_name, "nana/downloads/" + file_name)
    except OSError:
        return "Failed to download file\nInvaild file name!"
    return downlaoded


@app.on_message(filters.user(AdminSettings) & filters.command("dl", Command))
async def download_from_url(_client, message):
    if len(message.text.split()) == 1:
        await edrep(message, text="Usage: `dl <url> <filename>`")
        return
    if len(message.text.split()) == 2:
        url = message.text.split(None, 1)[1]
        file_name = url.split("/")[-1]
    elif len(message.text.split()) == 3:
        url = message.text.split(None, 2)[1]
        file_name = message.text.split(None, 2)[2]
    else:
        await edrep(message, text="Invaild args given!")
        return
    try:
        os.listdir("nana/downloads/")
    except FileNotFoundError:
        await edrep(message, text="Invalid download path in config!")
        return
    await edrep(message, text="Downloading...")
    download = await download_url(url, file_name)
    await edrep(message, text=download)


@app.on_message(filters.user(AdminSettings) & filters.command("download", Command))
async def dssownload_from_telegram(client, message):
    if message.reply_to_message:
        await download_file_from_tg(client, message)
    else:
        await edrep(message, text="Reply document to download it")


@app.on_message(filters.user(AdminSettings) & filters.command("direct", Command))
async def direct_link_generator(_client, message):
    args = message.text.split(None, 1)
    await edrep(message, text="`Processing...`")
    if len(args) == 1:
        await edrep(message, text="Write any args here!")
        return
    downloadurl = args[1]
    reply = ''
    links = re.findall(r'\bhttps?://.*\.\S+', downloadurl)
    if not links:
        reply = "`No links found!`"
        await edrep(message, text=reply)
    for link in links:
        if 'drive.google.com' in link:
            reply += gdrive(link)
        elif 'zippyshare.com' in link:
            reply += 'Zippy Share disabled of security reasons'
        elif 'yadi.sk' in link:
            reply += yandex_disk(link)
        elif 'mediafire.com' in link:
            reply += mediafire(link)
        elif 'sourceforge.net' in link:
            reply += sourceforge(link)
        elif 'osdn.net' in link:
            reply += osdn(link)
        elif 'github.com' in link:
            reply += github(link)
        elif 'androidfilehost.com' in link:
            reply += androidfilehost(link)
        else:
            reply += re.findall(r"\bhttps?://(.*?[^/]+)",
                                link)[0] + 'is not supported'
    await edrep(message, text=reply)


def gdrive(url: str) -> str:
    """GDrive direct links generator"""
    drive = 'https://drive.google.com'
    try:
        link = re.findall(r'\bhttps?://drive\.google\.com\S+', url)[0]
    except IndexError:
        reply = "`No Google drive links found`\n"
        return reply
    file_id = ''
    reply = ''
    if link.find("view") != -1:
        file_id = link.split('/')[-2]
    elif link.find("open?id=") != -1:
        file_id = link.split("open?id=")[1].strip()
    elif link.find("uc?id=") != -1:
        file_id = link.split("uc?id=")[1].strip()
    url = f'{drive}/uc?export=download&id={file_id}'
    download = requests.get(url, stream=True, allow_redirects=False)
    cookies = download.cookies
    try:
        # In case of small file size, Google downloads directly
        dl_url = download.headers["location"]
        if 'accounts.google.com' in dl_url:  # non-public file
            reply += '`Link is not public!`\n'
            return reply
        name = 'Direct Download Link'
    except KeyError:
        # In case of download warning page
        page = BeautifulSoup(download.content, 'lxml')
        export = drive + page.find('a', {'id': 'uc-download-link'}).get('href')
        name = page.find('span', {'class': 'uc-name-size'}).text
        response = requests.get(export,
                                stream=True,
                                allow_redirects=False,
                                cookies=cookies)
        dl_url = response.headers['location']
        if 'accounts.google.com' in dl_url:
            reply += 'Link is not public!'
            return reply
    reply += f'[{name}]({dl_url})\n'
    return reply


def yandex_disk(url: str) -> str:
    """Yandex.Disk direct links generator"""
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*yadi\.sk\S+', url)[0]
    except IndexError:
        reply = "`No Yandex.Disk links found`\n"
        return reply
    api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
    try:
        dl_url = requests.get(api.format(link)).json()['href']
        name = dl_url.split('filename=')[1].split('&disposition')[0]
        reply += f'[{name}]({dl_url})\n'
    except KeyError:
        reply += '`Error: File not found / Download limit reached`\n'
        return reply
    return reply


def mediafire(url: str) -> str:
    """MediaFire direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*mediafire\.com\S+', url)[0]
    except IndexError:
        reply = "`No MediaFire links found`\n"
        return reply
    reply = ''
    page = BeautifulSoup(requests.get(link).content, 'lxml')
    info = page.find('a', {'aria-label': 'Download file'})
    dl_url = info.get('href')
    size = re.findall(r'\(.*\)', info.text)[0]
    name = page.find('div', {'class': 'filename'}).text
    reply += f'[{name} {size}]({dl_url})\n'
    return reply


def sourceforge(url: str) -> str:
    """SourceForge direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*sourceforge\.net\S+', url)[0]
    except IndexError:
        reply = "`No SourceForge links found`\n"
        return reply
    file_path = re.findall(r'files(.*)/download', link)[0]
    reply = f"Mirrors for __{file_path.split('/')[-1]}__\n"
    project = re.findall(r'projects?/(.*?)/files', link)[0]
    mirrors = f'https://sourceforge.net/settings/mirror_choices?' \
              f'projectname={project}&filename={file_path}'
    page = BeautifulSoup(requests.get(mirrors).content, 'html.parser')
    info = page.find('ul', {'id': 'mirrorList'}).findAll('li')
    for mirror in info[1:]:
        name = re.findall(r'\((.*)\)', mirror.text.strip())[0]
        dl_url = f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        reply += f'[{name}]({dl_url}) '
    return reply


def osdn(url: str) -> str:
    """OSDN direct links generator"""
    osdn_link = 'https://osdn.net'
    try:
        link = re.findall(r'\bhttps?://.*osdn\.net\S+', url)[0]
    except IndexError:
        reply = "`No OSDN links found`\n"
        return reply
    page = BeautifulSoup(
        requests.get(link, allow_redirects=True).content, 'lxml')
    info = page.find('a', {'class': 'mirror_link'})
    link = urllib.parse.unquote(osdn_link + info['href'])
    reply = f"Mirrors for __{link.split('/')[-1]}__\n"
    mirrors = page.find('form', {'id': 'mirror-select-form'}).findAll('tr')
    for data in mirrors[1:]:
        mirror = data.find('input')['value']
        name = re.findall(r'\((.*)\)', data.findAll('td')[-1].text.strip())[0]
        dl_url = re.sub(r'm=(.*)&f', f'm={mirror}&f', link)
        reply += f'[{name}]({dl_url}) '
    return reply


def github(url: str) -> str:
    """GitHub direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*github\.com.*releases\S+', url)[0]
    except IndexError:
        reply = "`No GitHub Releases links found`\n"
        return reply
    reply = ''
    dl_url = ''
    download = requests.get(url, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
    except KeyError:
        reply += "`Error: Can't extract the link`\n"
    name = link.split('/')[-1]
    reply += f'[{name}]({dl_url}) '
    return reply


def androidfilehost(url: str) -> str:
    """AFH direct links generator"""
    try:
        link = re.findall(r'\bhttps?://.*androidfilehost.*fid.*\S+', url)[0]
    except IndexError:
        reply = "`No AFH links found`\n"
        return reply
    fid = re.findall(r'\?fid=(.*)', link)[0]
    session = requests.Session()
    user_agent = useragent()
    headers = {'user-agent': user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        'origin': 'https://androidfilehost.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': user_agent,
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-mod-sbb-ctype': 'xhr',
        'accept': '*/*',
        'referer': f'https://androidfilehost.com/?fid={fid}',
        'authority': 'androidfilehost.com',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'submit': 'submit',
        'action': 'getdownloadmirrors',
        'fid': f'{fid}'
    }
    mirrors = None
    reply = ''
    error = "`Error: Can't find Mirrors for the link`\n"
    try:
        req = session.post(
            'https://androidfilehost.com/libs/otf/mirrors.otf.php',
            headers=headers,
            data=data,
            cookies=res.cookies)
        mirrors = req.json()['MIRRORS']
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item['name']
        dl_url = item['url']
        reply += f'[{name}]({dl_url}) '
    return reply


def useragent():
    """useragent random setter"""
    useragents = BeautifulSoup(
        requests.get(
            'https://developers.whatismybrowser.com/'
            'useragents/explore/operating_system_name/android/').content,
        'lxml').findAll('td', {'class': 'useragent'})
    user_agent = choice(useragents)
    return user_agent.text


async def progressdl(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}] {2}%\n".format(
            ''.join("▰" for i in range(math.floor(percentage / 10))),
            ''.join("▱" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2))
        tmp = progress_str + \
              "{0} of {1}\nETA: {2}".format(
                  humanbytes(current),
                  humanbytes(total),
                  await time_formatter(estimated_total_time)
              )
        if file_name:
            await event.edit("{}\nFile Name: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Input size in bytes"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " day(s), ") if days else "") + \
          ((str(hours) + " hour(s), ") if hours else "") + \
          ((str(minutes) + " minute(s), ") if minutes else "") + \
          ((str(seconds) + " second(s), ") if seconds else "") + \
          ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    return tmp[:-2]


async def download_reply_nocall(client, message):
	if message.reply_to_message.photo:
		nama = "photo_{}_{}.png".format(message.reply_to_message.photo.file_id, message.reply_to_message.photo.date)
		await client.download_media(message.reply_to_message.photo, file_name="nana/downloads/" + nama)
	elif message.reply_to_message.animation:
		nama = "giphy_{}-{}.gif".format(message.reply_to_message.animation.date, message.reply_to_message.animation.file_size)
		await client.download_media(message.reply_to_message.animation, file_name="nana/downloads/" + nama)
	elif message.reply_to_message.video:
		nama = "video_{}-{}.mp4".format(message.reply_to_message.video.date, message.reply_to_message.video.file_size)
		await client.download_media(message.reply_to_message.video, file_name="nana/downloads/" + nama)
	elif message.reply_to_message.sticker:
		nama = "sticker_{}_{}.webp".format(message.reply_to_message.sticker.date, message.reply_to_message.sticker.set_name)
		await client.download_media(message.reply_to_message.sticker, file_name="nana/downloads/" + nama)
	elif message.reply_to_message.audio:
		nama = "{}".format(message.reply_to_message.audio.file_name)
		await client.download_media(message.reply_to_message.audio, file_name="nana/downloads/" + nama)
	elif message.reply_to_message.voice:
		nama = "audio_{}.ogg".format(message.reply_to_message.voice.date)
		await client.download_media(message.reply_to_message.voice, file_name="nana/downloads/" + nama)
	elif message.reply_to_message.document:
		nama = "{}".format(message.reply_to_message.document.file_name)
		await client.download_media(message.reply_to_message.document, file_name="nana/downloads/" + nama)
	else:
		return False
	return "nana/downloads/" + nama


async def download_file_from_tg(client, message):
    start = int(time.time())
    c_time = time.time()
    name = await name_file(client, message)
    if message.reply_to_message.photo:
        await client.download_media(message.reply_to_message.photo, file_name="nana/downloads/" + name,
                                    progress=lambda d, t: asyncio.get_event_loop().create_task(
                                        progressdl(d, t, message, c_time, "Downloading...")))
    elif message.reply_to_message.animation:
        await client.download_media(message.reply_to_message.animation, file_name="nana/downloads/" + name,
                                    progress=lambda d, t: asyncio.get_event_loop().create_task(
                                        progressdl(d, t, message, c_time, "Downloading...")))
    elif message.reply_to_message.video:
        await client.download_media(message.reply_to_message.video, file_name="nana/downloads/" + name,
                                    progress=lambda d, t: asyncio.get_event_loop().create_task(
                                        progressdl(d, t, message, c_time, "Downloading...")))
    elif message.reply_to_message.sticker:
        await client.download_media(message.reply_to_message.sticker, file_name="nana/downloads/" + name,
                                    progress=lambda d, t: asyncio.get_event_loop().create_task(
                                        progressdl(d, t, message, c_time, "Downloading...")))
    elif message.reply_to_message.audio:
        await client.download_media(message.reply_to_message.audio, file_name="nana/downloads/" + name,
                                    progress=lambda d, t: asyncio.get_event_loop().create_task(
                                        progressdl(d, t, message, c_time, "Downloading...")))
    elif message.reply_to_message.voice:
        await client.download_media(message.reply_to_message.voice, file_name="nana/downloads/" + name,
                                    progress=lambda d, t: asyncio.get_event_loop().create_task(
                                        progressdl(d, t, message, c_time, "Downloading...")))
    elif message.reply_to_message.document:
        await client.download_media(message.reply_to_message.document, file_name="nana/downloads/" + name,
                                    progress=lambda d, t: asyncio.get_event_loop().create_task(
                                        progressdl(d, t, message, c_time, "Downloading...")))
    else:
        await edrep(message, text="Unknown file!")
        return
    end = int(time.time())
    times = await time_parser(start, end)
    text = f"**⬇ Downloaded!**\n🗂 File name: `{name}`\n🏷 Saved to: `nana/downloads/`\n⏲ Downloaded in: {times}"
    await edrep(message, text=text)


async def name_file(_client, message):
    if message.reply_to_message.photo:
        return "photo_{}_{}.png".format(message.reply_to_message.photo.date,
                                        message.reply_to_message.photo.date)
    elif message.reply_to_message.animation:
        return "giphy_{}-{}.gif".format(message.reply_to_message.animation.date,
                                        message.reply_to_message.animation.file_size)
    elif message.reply_to_message.video:
        return "video_{}-{}.mp4".format(message.reply_to_message.video.date,
                                        message.reply_to_message.video.file_size)
    elif message.reply_to_message.sticker:
        return "sticker_{}_{}.webp".format(message.reply_to_message.sticker.date,
                                           message.reply_to_message.sticker.set_name)
    elif message.reply_to_message.audio:
        return "{}".format(message.reply_to_message.audio.file_name)
    elif message.reply_to_message.voice:
        return "audio_{}.ogg".format(message.reply_to_message.voice.date)
    elif message.reply_to_message.document:
        return "{}".format(message.reply_to_message.document.file_name)
    else:
        await edrep(message, text="Unknown file!")
        return
