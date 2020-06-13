import logging
import os
import re
import shutil
import subprocess
import sys
import traceback

import pafy
import requests
from bs4 import BeautifulSoup
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton
from pytube import YouTube

from nana import app, setbot, Command
from nana.helpers.parser import escape_markdown
from nana.modules.downloads import download_url

__MODULE__ = "YouTube"
__HELP__ = """
Search, download, convert music from youtube!
Enjoy~

──「 **Search video** 」──
-> `youtube (text)`
-> `yt (text)`
Give text as args for search from youtube, will send result more than 10 depending on yt page.

──「 **Download video** 」──
-> `ytdl (url) (resolution*)`
Download youtube video (mp4), resolution is optional. use resolution under 240p result video will send gif format

──「 **Convert to music** 」──
-> `ytmusic (url)`
-> `ytaudio (url)`
Download youtube music, and then send to tg as music.
"""


@app.on_message(Filters.user("self") & Filters.command(["youtube", "yt"], Command))
async def youtube_search(_client, message):
	args = message.text.split(None, 1)
	if len(args) == 1:
		await message.edit("Write any args here!")
		return
	teks = args[1]
	responce = requests.get('https://www.youtube.com/results?search_query=' + teks.replace(" ", "%20"))
	soup = BeautifulSoup(responce.content, "html.parser")
	divs = soup.find_all("div", {"class": "yt-lockup"})
	yutub = "<b>Results of {}</b>\n".format(teks)
	nomor = 0
	for i in divs:
		title = i.find('h3', {'class': "yt-lockup-title"}).a.get('title')
		url = i.find('h3', {'class': "yt-lockup-title"}).a.get('href')
		vidtime = i.find("span", {"class": "video-time"})
		if vidtime:
			vidtime = str("(" + vidtime.text + ")")
		else:
			vidtime = ""
		nomor += 1
		yutub += '<b>{}.</b> <a href="{}">{}</a> {}\n'.format(nomor, "https://www.youtube.com" + url, title, vidtime)
	await message.edit(yutub, disable_web_page_preview=True, parse_mode="html")


@app.on_message(Filters.user("self") & Filters.command(["ytdl"], Command))
async def youtube_download(_client, message):
	args = message.text.split(None, 2)
	await message.edit("Checking")
	if len(args) == 1:
		await message.edit("Write any args here!")
		return
	try:
		yt = YouTube(args[1])
	except ValueError:
		await message.edit("Invalid URL!")
		return

	if len(args) == 2:
		link = args[1]
		text = "🎬 **Title:** [{}]({})\n".format(escape_markdown(yt.title), link)
		status = "**Downloading video...**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		YouTube(link).streams.first().download('nana/downloads', filename="tempvid")
		status = "**Uploading File To Telegram...**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		await app.send_video(message.chat.id, video="nana/downloads/tempvid.mp4")
		status = "**Removing Temp File...**"
		await message.edit(status)
		os.remove('nana/downloads/tempvid.mp4')
		status = "** Done ✔️✔️**\n"
		await message.edit(status + text, disable_web_page_preview=True)

		return
	if len(args) == 3:
		link = args[1]
		reso = args[2]
		text = "🎬 **Title:** [{}]({})\n".format(escape_markdown(yt.title), link)
		status = "**Downloading video...**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		stream = yt.streams.filter(file_extension='mp4').filter(resolution="{}".format(reso)).first()
		stream.download('nana/downloads', filename="tempvid")
		status = "**Uploading File To Telegram...**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		await app.send_video(message.chat.id, video="nana/downloads/tempvid.mp4")
		status = "**Removing Temp File...**"
		await message.edit(status)
		os.remove('nana/downloads/tempvid.mp4')
		status = "**Done ✔️✔️**\n"
		await message.edit(status + text, disable_web_page_preview=True)
		return


@app.on_message(Filters.user("self") & Filters.command(["ytmusic", "ytaudio"], Command))
async def youtube_music(_client, message):
	args = message.text.split(None, 1)
	if len(args) == 1:
		await message.edit("Send URL here!")
		return
	teks = args[1]
	try:
		video = pafy.new(teks)
	except ValueError:
		await message.edit("Invaild URL!")
		return
	try:
		audios = [audio for audio in video.audiostreams]
		audios.sort(key=lambda a: (int(a.quality.strip('k')) * -1))
		music = audios[0]
		text = "[⁣](https://i.ytimg.com/vi/{}/0.jpg)🎬 **Title:** [{}]({})\n".format(video.videoid,
																					escape_markdown(video.title),
																					video.watchv_url
																				)
		text += "👤 **Author:** `{}`\n".format(video.author)
		text += "🕦 **Duration:** `{}`\n".format(video.duration)
		origtitle = re.sub(r'[\\/*?:"<>|\[\]]', "", str(music.title + "." + music._extension))
		musictitle = re.sub(r'[\\/*?:"<>|\[\]]', "", str(music.title))
		musicdate = video._ydl_info['upload_date'][:4]
		titletext = "**Downloading music...**\n"
		await message.edit(titletext + text, disable_web_page_preview=False)
		r = requests.get("https://i.ytimg.com/vi/{}/maxresdefault.jpg".format(video.videoid), stream=True)
		if r.status_code != 200:
			r = requests.get("https://i.ytimg.com/vi/{}/hqdefault.jpg".format(video.videoid), stream=True)
			if r.status_code != 200:
				r = requests.get("https://i.ytimg.com/vi/{}/sddefault.jpg".format(video.videoid), stream=True)
				if r.status_code != 200:
					r = requests.get("https://i.ytimg.com/vi/{}/mqdefault.jpg".format(video.videoid), stream=True)
					if r.status_code != 200:
						r = requests.get("https://i.ytimg.com/vi/{}/default.jpg".format(video.videoid), stream=True)
						if r.status_code != 200:
							avthumb = False
		if r.status_code == 200:
			avthumb = True
			with open("nana/cache/thumb.jpg", "wb") as stk:
				shutil.copyfileobj(r.raw, stk)
		try:
			os.remove("nana/downloads/{}".format(origtitle))
		except FileNotFoundError:
			pass
		# music.download(filepath="nana/downloads/{}".format(origtitle))
		if "manifest.googlevideo.com" in music.url:
			download = await download_url(music._info['fragment_base_url'], origtitle)
		else:
			download = await download_url(music.url, origtitle)
		if download == "Failed to download file\nInvaild file name!":
			return await message.edit(download)
		titletext = "**Converting music...**\n"
		await message.edit(titletext + text, disable_web_page_preview=False)
		try:
			subprocess.Popen("ffmpeg", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except Exception as err:
			if "The system cannot find the file specified" in str(err) or "No such file or directory" in str(err):
				await message.edit("You need to install ffmpeg first!\nCheck your assistant for more information!")
				await setbot.send_message(message.from_user.id,
										"Hello 🙂\nYou need to install ffmpeg to make audio works better, here is guide how to install it:\n\n**If you're using linux**, go to your terminal, type:\n`sudo apt install ffmpeg`\n\n**If you're using Windows**, download ffmpeg here:\n`https://ffmpeg.zeranoe.com/builds/`\nAnd then extract (if was archive), and place ffmpeg.exe to workdir (in current dir)\n\n**If you're using heroku**, type this in your workdir:\n`heroku buildpacks:add https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`\nOr if you not using heroku term, follow this guide:\n1. Go to heroku.com\n2. Go to your app in heroku\n3. Change tabs/click Settings, then search for Buildpacks text\n4. Click button Add build pack, then type `https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`\n5. Click Save changes, and you need to rebuild your heroku app to take changes!\n\nNeed help?\nGo @nanabotsupport and ask there")
				return
		if avthumb:
			os.system(
				f'ffmpeg -loglevel panic -i "nana/downloads/{origtitle}" -i "nana/cache/thumb.jpg" -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" -metadata title="{music.title}" -metadata author="{video.author}" -metadata album="{video.author}" -metadata album_artist="{video.author}" -metadata genre="{video._category}" -metadata date="{musicdate}" -acodec libmp3lame -aq 4 -y "nana/downloads/{musictitle}.mp3"')
		else:
			os.system(
				f'ffmpeg -loglevel panic -i "nana/downloads/{origtitle}" -metadata title="{music.title}" -metadata author="{video.author}" -metadata album="{video.author}" -metadata album_artist="{video.author}" -metadata genre="{video._category}" -metadata date="{musicdate}" -acodec libmp3lame -aq 4 -y "nana/downloads/{musictitle}.mp3"')
		try:
			os.remove("nana/downloads/{}".format(origtitle))
		except FileNotFoundError:
			pass
		titletext = "**Uploading...**\n"
		await message.edit(titletext + text, disable_web_page_preview=False)
		getprev = requests.get(video.thumb, stream=True)
		with open("nana/cache/prev.jpg", "wb") as stk:
			shutil.copyfileobj(getprev.raw, stk)
		await app.send_audio(message.chat.id, audio="nana/downloads/{}.mp3".format(musictitle),
							thumb="nana/cache/prev.jpg", title=music.title, caption="🕦 `{}`".format(video.duration),
							reply_to_message_id=message.message_id
						)
		try:
			os.remove("nana/cache/prev.jpg")
		except FileNotFoundError:
			pass
		try:
			os.remove("nana/cache/thumb.jpg")
		except FileNotFoundError:
			pass
		titletext = "**Done! 🤗**\n"
		await message.edit(titletext + text, disable_web_page_preview=False)
	except Exception as err:
		if "command not found" in str(err) or "is not recognized" in str(err):
			await message.edit("You need to install ffmpeg first!\nCheck your assistant for more information!")
			await setbot.send_message(message.from_user.id,
									"Hello 🙂\nYou need to install ffmpeg to make audio works better, here is guide "
									"how to install it:\n\n**If you're using linux**, go to your terminal, "
									"type:\n`sudo apt install ffmpeg`\n\n**If you're using Windows**, download "
									"ffmpeg here:\n`https://ffmpeg.zeranoe.com/builds/`\nAnd then extract (if was "
									"archive), and place ffmpeg.exe to workdir (in current dir)\n\n**If you're using "
									"heroku**, type this in your workdir:\n`heroku buildpacks:add "
									"https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`\nOr if you "
									"not using heroku term, follow this guide:\n1. Go to heroku.com\n2. Go to your "
									"app in heroku\n3. Change tabs/click Settings, then search for Buildpacks "
									"text\n4. Click button Add build pack, then type "
									"`https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest`\n5. Click Save "
									"changes, and you need to rebuild your heroku app to take changes!\n\nNeed "
									"help?\nGo @AyraSupport and ask there")
			return
		exc_type, exc_obj, exc_tb = sys.exc_info()
		errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
		await message.edit("**An error has accured!**\nCheck your assistant for more information!")
		button = InlineKeyboardMarkup([[InlineKeyboardButton("🐞 Report bugs", callback_data="report_errors")]])
		await setbot.send_message(message.from_user.id, "**An error has accured!**\n```{}```".format("".join(errors)),
								reply_markup=button)
		logging.exception("Execution error")
