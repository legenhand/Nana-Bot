import time
import datetime
import os

from os import popen
import re
import urllib.parse
import json
from random import choice
import requests
from bs4 import BeautifulSoup
from humanize import naturalsize

from nana import app, Command
from pyrogram import Filters
from pyDownload import Downloader

__MODULE__ = "Downloads"
__HELP__ = """
Download any file from URL or from telegram

──「 **Download From URL** 」──
-> `dl (url)`
Give url as args to download it.

──「 **Download From Telegram** 」──
-> `download`
Reply a document to download it.

──「 **Direct Link Download** 」──
-> `direct (url)`
Create A direct link download

Supported Link
`gdrive  | zippyshare   | mega
yadi.sk | cloud.mail.ru| mediafire
osdn.net| Sourceforge  | github.com
androidfilehost.com`
"""


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
    elif size > 1024000 and size < 1024000000:
        file_size = round(size / 1024000, 3)
        downlaoded += "\n💿 File size: `" + str(file_size) + " MB`\n"
    elif size > 1024 and size < 1024000:
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


@app.on_message(Filters.user("self") & Filters.command(["dl"], Command))
async def download_from_url(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `dl <url> <filename>`")
        return
    if len(message.text.split()) == 2:
        URL = message.text.split(None, 1)[1]
        file_name = URL.split("/")[-1]
    elif len(message.text.split()) == 3:
        URL = message.text.split(None, 2)[1]
        file_name = message.text.split(None, 2)[2]
    else:
        await message.edit("Invaild args given!")
        return
    try:
        os.listdir("nana/downloads/")
    except FileNotFoundError:
        await message.edit("Invalid download path in config!")
        return
    await message.edit("Downloading...")
    download = await download_url(URL, file_name)
    await message.edit(download)


@app.on_message(Filters.user("self") & Filters.command(["download"], Command))
async def download_from_telegram(client, message):
    if message.reply_to_message:
        await message.edit("__Downloading...__")
        start = int(time.time())
        if message.reply_to_message.photo:
            nama = "photo_{}_{}.png".format(message.reply_to_message.photo, message.reply_to_message.photo.date)
            await client.download_media(message.reply_to_message.photo, file_name="nana/downloads/" + nama)
        elif message.reply_to_message.animation:
            nama = "giphy_{}-{}.gif".format(message.reply_to_message.animation.date,
                                            message.reply_to_message.animation.file_size)
            await client.download_media(message.reply_to_message.animation, file_name="nana/downloads/" + nama)
        elif message.reply_to_message.video:
            nama = "video_{}-{}.mp4".format(message.reply_to_message.video.date,
                                            message.reply_to_message.video.file_size)
            await client.download_media(message.reply_to_message.video, file_name="nana/downloads/" + nama)
        elif message.reply_to_message.sticker:
            nama = "sticker_{}_{}.webp".format(message.reply_to_message.sticker.date,
                                               message.reply_to_message.sticker.set_name)
            await client.download_media(message.reply_to_message.sticker, file_name="nana/downloads/" + nama)
        elif message.reply_to_message.audio:
            nama = "{}".format(message.reply_to_message.audio.file_name)
            await client.download_media(message.reply_to_message.audio, file_name="nana/downloads/" + nama)
        elif message.reply_to_message.voice:
            nama = "audio_{}.ogg".format(message.reply_to_message.voice)
            await client.download_media(message.reply_to_message.voice, file_name="nana/downloads/" + nama)
        elif message.reply_to_message.document:
            nama = "{}".format(message.reply_to_message.document.file_name)
            await client.download_media(message.reply_to_message.document, file_name="nana/downloads/" + nama)
        else:
            await message.edit("Unknown file!")
            return
        end = int(time.time())
        times = await time_parser(start, end)
        text = f"**⬇ Downloaded!**\n🗂 File name: `{nama}`\n🏷 Saved to: `nana/downloads/`\n⏲ Downloaded in: {times}"
        await message.edit(text)
    else:
        await message.edit("Reply document to download it")


@app.on_message(Filters.user("self") & Filters.command(["direct"], Command))
async def direct_link_generator(client, message):
    args = message.text.split(None, 1)
    await message.edit("`Processing...`")
    if len(args) == 1:
        await message.edit("Write any args here!")
        return
    downloadurl = args[1]
    reply = ''
    links = re.findall(r'\bhttps?://.*\.\S+', downloadurl)
    if not links:
        reply = "`No links found!`"
        await message.edit(reply)
    for link in links:
        if 'drive.google.com' in link:
            reply += gdrive(link)
        elif 'zippyshare.com' in link:
            reply += zippy_share(link)
        elif 'mega.' in link:
            reply += mega_dl(link)
        elif 'yadi.sk' in link:
            reply += yandex_disk(link)
        elif 'cloud.mail.ru' in link:
            reply += cm_ru(link)
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
    await message.edit(reply)


def gdrive(url: str) -> str:
    """ GDrive direct links generator """
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


def zippy_share(url: str) -> str:
    """ ZippyShare direct links generator
    Based on https://github.com/LameLemon/ziggy"""
    reply = ''
    dl_url = ''
    try:
        link = re.findall(r'\bhttps?://.*zippyshare\.com\S+', url)[0]
    except IndexError:
        reply = "`No ZippyShare links found`\n"
        return reply
    session = requests.Session()
    base_url = re.search('http.+.com', link).group()
    response = session.get(link)
    page_soup = BeautifulSoup(response.content, "lxml")
    scripts = page_soup.find_all("script", {"type": "text/javascript"})
    for script in scripts:
        if "getElementById('dlbutton')" in script.text:
            url_raw = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                                script.text).group('url')
            math = re.search(r'= (?P<url>\".+\" \+ (?P<math>\(.+\)) .+);',
                             script.text).group('math')
            dl_url = url_raw.replace(math, '"' + str(eval(math)) + '"')
            break
    dl_url = base_url + eval(dl_url)
    name = urllib.parse.unquote(dl_url.split('/')[-1])
    reply += f'[{name}]({dl_url})\n'
    return reply


def yandex_disk(url: str) -> str:
    """ Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
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


def mega_dl(url: str) -> str:
    """ MEGA.nz direct links generator
    Using https://github.com/tonikelope/megadown"""
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*mega.*\.nz\S+', url)[0]
    except IndexError:
        reply = "`No MEGA.nz links found`\n"
        return reply
    command = f'bin/megadown -q -m {link}'
    result = popen(command).read()
    try:
        data = json.loads(result)
        print(data)
    except json.JSONDecodeError:
        reply += "`Error: Can't extract the link`\n"
        return reply
    dl_url = data['url']
    name = data['file_name']
    size = naturalsize(int(data['file_size']))
    reply += f'[{name} ({size})]({dl_url})\n'
    return reply


def cm_ru(url: str) -> str:
    """ cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    reply = ''
    try:
        link = re.findall(r'\bhttps?://.*cloud\.mail\.ru\S+', url)[0]
    except IndexError:
        reply = "`No cloud.mail.ru links found`\n"
        return reply
    command = f'bin/cmrudl -s {link}'
    result = popen(command).read()
    result = result.splitlines()[-1]
    try:
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        reply += "`Error: Can't extract the link`\n"
        return reply
    dl_url = data['download']
    name = data['file_name']
    size = naturalsize(int(data['file_size']))
    reply += f'[{name} ({size})]({dl_url})\n'
    return reply


def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
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
    """ SourceForge direct links generator """
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
    """ OSDN direct links generator """
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
    """ GitHub direct links generator """
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
    """ AFH direct links generator """
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
    """
    useragent random setter
    """
    useragents = BeautifulSoup(
        requests.get(
            'https://developers.whatismybrowser.com/'
            'useragents/explore/operating_system_name/android/').content,
        'lxml').findAll('td', {'class': 'useragent'})
    user_agent = choice(useragents)
    return user_agent.text
