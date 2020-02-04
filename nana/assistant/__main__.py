import os, requests

from bs4 import BeautifulSoup
from platform import python_version, uname

from nana import app, setbot, Owner, AdminSettings, DB_AVAIABLE, USERBOT_VERSION, ASSISTANT_VERSION, BotUsername
from __main__ import reload_userbot, restart_all
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, errors

from threading import Thread


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["start"]))
async def start(client, message):
	if len(message.text.split()) >= 2:
		helparg = message.text.split()[1]
		if helparg == "help_inline":
			await message.reply("""**Inline Guide**
Just type `@{} (command)` in text box, and wait for response.

──「 **Get Note from Inline** 」──
-> `#note <*notetag>`
And wait for list of notes in inline, currently support Text and Button only.

──「 **Stylish Generator Inline** 」──
-> `#stylish your text`
Convert a text to various style, can be used anywhere!

* = Can be used as optional
""".format(BotUsername))
			return
		if helparg == "createown":
			await message.reply("Want to create your own Userbot and Assistant?\n[Go here](https://github.com/AyraHikari/Nana-TgBot/wiki), read guide carefully.\nIf you want to ask, join our community @AyraSupport")
			return
	try:
		me = await app.get_me()
	except ConnectionError:
		me = None
	text = "Hello {}!\n".format(message.from_user.first_name)
	text += "**Here is your current stats:**\n"
	if not me:
		text += "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
	else:
		text += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
	text += "-> Assistant: `Running (v{})`\n".format(ASSISTANT_VERSION)
	text += "-> Database: `{}`\n".format(DB_AVAIABLE)
	text += "-> Python: `{}`\n".format(python_version())
	if not me:
		text += "\nBot is currently turned off, to start bot again, type /settings and click **Start Bot** button"
	else:
		text += "\nBot logged in as `{}`\nTo get more information about this user, type /getme\n".format(me.first_name)
	await message.reply(text)

@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["getme"]))
async def get_myself(client, message):
	try:
		me = await app.get_me()
	except ConnectionError:
		message.reply("Bot is currently turned off!")
		return
	getphoto = await client.get_profile_photos(me.id)
	if len(getphoto) == 0:
		getpp = None
	else:
		getpp = getphoto[0].file_id
	text = "**ℹ️ Your profile:**\n"
	text += "First name: {}\n".format(me.first_name)
	if me.last_name:
		text += "Last name: {}\n".format(me.last_name)
	text += "User ID: `{}`\n".format(me.id)
	if me.username:
		text += "Username: @{}\n".format(me.username)
	text += "Phone number: `{}`\n".format(me.phone_number)
	text += "`Nana Version    : v{}`\n".format(USERBOT_VERSION)
	text += "`Manager Version : v{}`".format(ASSISTANT_VERSION)
	button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])
	if me.photo:
		await client.send_photo(message.chat.id, photo=getpp, caption=text, reply_markup=button)
	else:
		await message.reply(text, reply_markup=button)


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["settings"]))
async def settings(client, message):
	try:
		me = await app.get_me()
	except ConnectionError:
		me = None
	text = "**⚙️ Welcome to Nana Settings!**\n"
	if not me:
		text += "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
	else:
		text += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
	text += "-> Assistant: `Running (v{})`\n".format(ASSISTANT_VERSION)
	text += "-> Database: `{}`\n".format(DB_AVAIABLE)
	text += "-> Python: `{}`\n".format(python_version())
	text += "\nJust setup what you need here"
	if not me:
		togglestart = "Start Bot"
	else:
		togglestart = "Stop Bot"
	button = InlineKeyboardMarkup([[InlineKeyboardButton(togglestart, callback_data="toggle_startbot"), InlineKeyboardButton("Restart Bot", callback_data="restart_bot")]])
	await message.reply(text, reply_markup=button)


# For callback query button
def dynamic_data_filter(data):
	return Filters.create(
		lambda flt, query: flt.data == query.data,
		data=data  # "data" kwarg is accessed with "flt.data" above
	)

@setbot.on_callback_query(dynamic_data_filter("hide_number"))
async def get_myself_btn(client, query):
	try:
		me = await app.get_me()
	except ConnectionError:
		await client.answer_callback_query(query.id, "Bot is currently turned off!", show_alert=True)
		return

	if query.message.caption:
		text = query.message.caption.markdown
	else:
		text = query.message.text.markdown

	num = []
	num.append("*"*len(me.phone_number))

	if "***" not in text.split("Phone number: `")[1].split("`")[0]:
		text = text.replace("Phone number: `{}`\n".format(me.phone_number), "Phone number: `{}`\n".format("".join(num)))
		button = InlineKeyboardMarkup([[InlineKeyboardButton("Show phone number", callback_data="hide_number")]])
	else:
		text = text.replace("Phone number: `{}`\n".format("".join(num)), "Phone number: `{}`\n".format(me.phone_number))
		button = InlineKeyboardMarkup([[InlineKeyboardButton("Hide phone number", callback_data="hide_number")]])

	if query.message.caption:
		await query.message.edit_caption(caption=text, reply_markup=button)
	else:
		await query.message.edit(text, reply_markup=button)

@setbot.on_callback_query(dynamic_data_filter("toggle_startbot"))
async def start_stop_bot(client, query):
	try:
		me = await app.get_me()
	except ConnectionError:
		await reload_userbot()
		text = "**⚙️ Welcome to Nana Settings!**\n"
		text += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
		text += "-> Assistant: `Running (v{})`\n".format(ASSISTANT_VERSION)
		text += "-> Database: `{}`\n".format(DB_AVAIABLE)
		text += "-> Python: `{}`\n".format(python_version())
		text += "\n✅ Bot was started!"
		button = InlineKeyboardMarkup([[InlineKeyboardButton("Stop Bot", callback_data="toggle_startbot"), InlineKeyboardButton("Restart Bot", callback_data="restart_bot")]])
		try:
			await query.message.edit_text(text, reply_markup=button)
		except errors.exceptions.bad_request_400.MessageNotModified:
			pass
		await client.answer_callback_query(query.id, "Bot was started!")
		return
	await app.stop()
	text = "**⚙️ Welcome to Nana Settings!**\n"
	text += "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
	text += "-> Assistant: `Running (v{})`\n".format(ASSISTANT_VERSION)
	text += "-> Database: `{}`\n".format(DB_AVAIABLE)
	text += "-> Python: `{}`\n".format(python_version())
	text += "\n❎ Bot was stopped!"
	button = InlineKeyboardMarkup([[InlineKeyboardButton("Start Bot", callback_data="toggle_startbot"), InlineKeyboardButton("Restart Bot", callback_data="restart_bot")]])
	try:
		await query.message.edit_text(text, reply_markup=button)
	except errors.exceptions.bad_request_400.MessageNotModified:
		pass
	await client.answer_callback_query(query.id, "Bot was stopped!")


@setbot.on_callback_query(dynamic_data_filter("report_errors"))
async def report_some_errors(client, query):
	app.join_chat("@AyraSupport")
	text = "Hi @AyraHikari, i got an error for you.\nPlease take a look and fix it if possible.\n\nThank you ❤️"
	err = query.message.text
	open("nana/cache/errors.txt", "w").write(err)
	await query.message.edit_reply_markup(reply_markup=None)
	await app.send_document("AyraSupport", "nana/cache/errors.txt", caption=text)
	os.remove("nana/cache/errors.txt")
	await client.answer_callback_query(query.id, "Report was sent!")

@setbot.on_callback_query(dynamic_data_filter("restart_bot"))
async def reboot_bot(client, query):
	await restart_all()
	text = "**⚙️ Welcome to Nana Settings!**\n"
	text += "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
	text += "-> Assistant: `Running (v{})`\n".format(ASSISTANT_VERSION)
	text += "-> Database: `{}`\n".format(DB_AVAIABLE)
	text += "-> Python: `{}`\n".format(python_version())
	text += "\n✅ Bot was restarted!"
	button = InlineKeyboardMarkup([[InlineKeyboardButton("Stop Bot", callback_data="toggle_startbot"), InlineKeyboardButton("Restart Bot", callback_data="restart_bot")]])
	try:
		await query.message.edit_text(text, reply_markup=button)
	except errors.exceptions.bad_request_400.MessageNotModified:
		pass
	await client.answer_callback_query(query.id, "Please wait for bot restarting...")
