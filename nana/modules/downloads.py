import time
import datetime
import os

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
