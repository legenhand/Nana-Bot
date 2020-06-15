# Original Repo: https://github.com/AyraHikari/Nana-Userbot
# Give a star and follow ^_^
import os
import pyrogram
import math

from pyrogram.api import functions
from nana import app, Owner, Command, DB_AVAIABLE

from pyrogram import Filters
if DB_AVAIABLE:
	from nana.modules.database.cloner_db import backup_indentity, restore_identity

__MODULE__ = "Indentity Cloner"
__HELP__ = """
Download any file from URL or from telegram

──「 **Download From URL** 」──
-> `clone`
Reply to a user to clone Identity.

──「 **Download From Telegram** 」──
-> `revert`
Revert's to Original identity
"""

@app.on_message(Filters.me & Filters.command(["clone"], Command))
async def clone(client, message):
	if message.reply_to_message:
		target = message.reply_to_message.from_user.id
	elif len(message.text.split()) >= 2 and message.text.split()[1].isdigit():
		# TODO
		await message.edit("Select target user to clone their identity!")
	else:
		await message.edit("Select target user to clone their identity!")

	if "origin" in message.text:
		# Backup yours current identity
		my_self = await app.get_me()
		my_self = await client.send(functions.users.GetFullUser(id=await client.resolve_peer(my_self['id'])))

		# Backup my first name, last name, and bio
		backup_indentity(my_self['user']['first_name'], my_self['user']['last_name'], my_self['about'])

	# Get target pp
	q = await app.get_profile_photos(target)

	# Download it
	await client.download_media(q[0], file_name="nana/downloads/pp.png")

	# Set new pp
	await app.set_profile_photo("nana/downloads/pp.png")

	# Get target profile
	t = await app.get_users(target)
	t = await client.send(functions.users.GetFullUser(id=await client.resolve_peer(t['id'])))

	# Set new name
	await client.send(functions.account.UpdateProfile(first_name=t['user']['first_name'] if t['user']['first_name'] != None else "", last_name=t['user']['last_name'] if t['user']['last_name'] != None else "", about=t['about'] if t['about'] != None else ""))

	# Kaboom! Done!
	await message.edit("Kaboom!\nNew identity has changed!")


@app.on_message(Filters.me & Filters.command(["revert"], Command))
async def revert(client, message):
	first_name, last_name, bio = restore_identity()

	await client.send(functions.account.UpdateProfile(first_name=first_name if first_name != None else "", last_name=last_name if last_name != None else "", about=bio if bio != None else ""))

	photos = await app.get_profile_photos("me")

	await app.delete_profile_photos(photos[0].file_id)

	await message.edit("Kaboom!\nIts me again!")