import asyncio
import requests
import datetime
import os
import re
import shutil
import subprocess
import sys
import traceback

from nana import app, Command, logging
from nana.helpers.deldog import deldog
from nana.helpers.parser import mention_markdown
from pyrogram import Filters

__MODULE__ = "Devs"
__HELP__ = """
This command means for helping development

──「 **Execution** 」──
-> `exec (command)`
Execute a python commands.

──「 **Evaluation** 」──
-> `eval (command)`
Do math evaluation.

──「 **Command shell** 」──
-> `cmd (command)`
Execute command shell

──「 **Take log** 」──
-> `log`
Edit log message, or deldog instead

──「 **Get Data Center** 」──
-> `dc`
Get user specific data center
"""


async def stk(chat, photo):
	if "http" in photo:
		r = requests.get(photo, stream=True)
		with open("nana/cache/stiker.png", "wb") as stk:
			shutil.copyfileobj(r.raw, stk)
		await app.send_sticker(chat, "nana/cache/stiker.png")
		os.remove("nana/cache/stiker.png")
	else:
		await app.send_sticker(chat, photo)

async def vid(chat, video, caption=None):
	await app.send_video(chat, video, caption)

async def pic(chat, photo, caption=None):
	await app.send_photo(chat, photo, caption)

async def aexec(client, message, code):
	# Make an async function with the code and `exec` it
	exec(
		f'async def __ex(client, message): ' +
		''.join(f'\n {l}' for l in code.split('\n'))
	)

	# Get `__ex` from local variables, call it and return the result
	return await locals()['__ex'](client, message)

@app.on_message(Filters.user("self") & Filters.command(["exec"], Command))
async def executor(client, message):
	if len(message.text.split()) == 1:
		await message.edit("Usage: `exec message.edit('edited!')`")
		return
	args = message.text.split(None, 1)
	code = args[1]
	try:
		await aexec(client, message, code)
	except:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
		await message.edit("**Execute**\n`{}`\n\n**Failed:**\n```{}```".format(code, "".join(errors)))
		logging.exception("Execution error")


@app.on_message(Filters.user("self") & Filters.command(["cmd"], Command))
async def terminal(client, message):
	if len(message.text.split()) == 1:
		await message.edit("Usage: `cmd ping -c 5 google.com`")
		return
	args = message.text.split(None, 1)
	teks = args[1]
	if "\n" in teks:
		code = teks.split("\n")
		output = ""
		for x in code:
			shell = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', x)
			try:
				process = subprocess.Popen(
					shell,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
			except Exception as err: 
				await message.edit("""
**Input:**
```{}```

**Error:**
```{}```
""".format(teks, err))
			output += "**{}**\n".format(code)
			output += process.stdout.read()[:-1].decode("utf-8")
			output += "\n"
	else:
		shell = re.split(''' (?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', teks)
		for a in range(len(shell)):
			shell[a] = shell[a].replace('"', "")
		try:
			process = subprocess.Popen(
				shell,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
		except Exception as err:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
			await message.edit("""**Input:**\n```{}```\n\n**Error:**\n```{}```""".format(teks, "".join(errors)))
			return
		output = process.stdout.read()[:-1].decode("utf-8")
	if str(output) == "\n":
		output = None
	if output:
		if len(output) > 4096:
			file = open("nana/cache/output.txt", "w+")
			file.write(output)
			file.close()
			await client.send_document(message.chat.id, "nana/cache/output.txt", reply_to_message_id=message.message_id, caption="`Output file`")
			os.remove("nana/cache/output.txt")
			return
		await message.edit("""**Input:**\n```{}```\n\n**Output:**\n```{}```""".format(teks, output))
	else:
		await message.edit("**Input: **\n`{}`\n\n**Output: **\n`No Output`".format(teks))

@app.on_message(Filters.user("self") & Filters.command(["log"], Command))
async def log(client, message):
	try:
		await message.edit(str(message), parse_mode="")
	except:
		data = deldog(str(message))
		await message.edit(data)

@app.on_message(Filters.user("self") & Filters.command(["dc"], Command))
async def dc_id(client, message):
	chat = message.chat
	user = message.from_user
	if message.reply_to_message:
		if message.reply_to_message.forward_from:
			dc_id = await client.get_user_dc(message.reply_to_message.forward_from.id)
			user = mention_markdown(message.reply_to_message.forward_from.id, message.reply_to_message.forward_from.first_name)
		else:
			dc_id = await client.get_user_dc(message.reply_to_message.from_user.id)
			user = mention_markdown(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
	else:
		dc_id = await client.get_user_dc(message.from_user.id)
		user = mention_markdown(message.from_user.id, message.from_user.first_name)
	if dc_id == 1:
		text = "{}'s assigned datacenter is **DC1**, located in **MIA, Miami FL, USA**".format(user)
	elif dc_id == 2:
		text = "{}'s assigned datacenter is **DC2**, located in **AMS, Amsterdam, NL**".format(user)
	elif dc_id == 3:
		text = "{}'s assigned datacenter is **DC3**, located in **MIA, Miami FL, USA**".format(user)
	elif dc_id == 4:
		text = "{}'s assigned datacenter is **DC4**, located in **AMS, Amsterdam, NL**".format(user)
	elif dc_id == 5:
		text = "{}'s assigned datacenter is **DC5**, located in **SIN, Singapore, SG**".format(user)
	else:
		text = "{}'s assigned datacenter is **Unknown**".format(user)
	await message.edit(text)
