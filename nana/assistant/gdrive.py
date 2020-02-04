import os, time
import pydrive
from pydrive.drive import GoogleDrive

from nana import app, setbot, AdminSettings, gauth
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, errors
from __main__ import get_runtime
from nana.modules.chats import get_msgc


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["gdrive"]))
async def gdrive_helper(client, message):
	if len(message.text.split()) == 1:
		gdriveclient = os.path.isfile("client_secrets.json")
		if not gdriveclient:
			await message.reply("Hello, look like you're not logged in to google drive 🙂\nI can help you to login.\n\nFirst of all, you need to activate your google drive API\n1. [Go here](https://developers.google.com/drive/api/v3/quickstart/python), click **Enable the drive API**\n2. Login to your google account (skip this if you're already logged in)\n3. After logged in, click **Enable the drive API** again, and click **Download Client Configuration** button, download that.\n4. After downloaded that file, rename `credentials.json` to `client_secrets.json`, and upload to your bot dir (not in nana dir)\n\nAfter that, you can go next guide by type `/gdrive`")
			return
		gauth.LoadCredentialsFile("nana/session/drive")
		if gauth.credentials is None:
			authurl = gauth.GetAuthUrl()
			teks = "First, you must log in to your Google drive first.\n\n[Visit this link and login to your Google account]({})\n\nAfter that you will get a verification code, type `/gdrive (verification code)` without '(' or ')'.".format(authurl)
			await message.reply(teks)
			return
		await message.reply("You're already logged in!\nTo logout type `/gdrive logout`")
	elif len(message.text.split()) == 2 and message.text.split()[1] == "logout":
		os.remove("nana/session/drive")
		await message.reply("You have logged out of your account!\nTo login again, just type /gdrive")
	elif len(message.text.split()) == 2:
		try:
			gauth.Auth(message.text.split()[1])
		except pydrive.auth.AuthenticationError:
			await msg.reply_text("Kode autentikasi anda salah!")
			return
		gauth.SaveCredentialsFile("nana/session/drive")
		drive = GoogleDrive(gauth)
		file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
		for drivefolders in file_list:
			if drivefolders['title'] == 'Nana Drive':
				await message.reply("Authentication successful!\nWelcome back!")
				return
		mkdir = drive.CreateFile({'title': 'Nana Drive', "mimeType": "application/vnd.google-apps.folder"})
		mkdir.Upload()
		await message.reply("Authentication successful!\nThe 'Nana Drive' folder has been created automatically!")
	else:
		await message.reply("Invaild args!\nCheck /gdrive for usage guide")
