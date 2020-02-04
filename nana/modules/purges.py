import os
import pyrogram
import math

from nana import app, Owner, Command

from pyrogram import Filters

__MODULE__ = "Purges"
__HELP__ = """
Purge many messages in less than one seconds, you need to became admin to do this.
Except for purgeme feature

Do with you own risk!
Purges message will immediately purge that message without warning!

**「 DO NOT PLAY WITH THIS FEATURE 」**
THIS IS NOT A TROLL MODULE!
```
I am not responsible if you nuke all messages in your group, when purges
is running, none can stop that except restart your bot in terminal, but
that was too late, 1 second will purge over than 10000 messages, and
you're fucked off.
```
Developer create this module only for managing group, not for trolling user!
Read this before take an action!

-> All deleted message cannot restore
-> If you're not an admin, and purge with powerful number or reply first message of group, all of your message will deleted!
-> **DON'T DESTROY/DELETE ALL MESSAGES**, developer will not responsible if you're nuked your chat group. Except for cleaning group purposes.
-> This is not a joke, not funny if you're nuked a group by this feature and blame developer for made this powerful weapon!

Ok look like you're understand what happened if you playing with this powerful weapon.


──「 **Purge** 」──
-> `purge`
Purge from bellow to that replyed message, you need to became admins to do this, else it only purge your message only!
Give a number **without reply** to purge for x messages.

──「 **Purge My Messages** 」──
-> `purgeme`
Purge your messages only, no need admin permission.
"""

@app.on_message(Filters.user("self") & Filters.command(["purge"], Command))
async def purge(client, message):
	if message.reply_to_message:
		is_reply = True
		target = message.reply_to_message.message_id
	elif len(message.text.split()) >= 2 and message.text.split()[1].isdigit():
		is_reply = False
		target = int(message.text.split()[1])
	else:
		await message.edit("Reply to the message to purge until that, or give me a number!")
	if not is_reply:
		get_msg = await client.get_history(message.chat.id, limit=target+1)
		listall = [x.message_id for x in get_msg]
	else:
		dari = message.message_id + 1
		listall = [x for x in range(target, dari)]
		listall.reverse()
	if len(listall) >= 101:
		total = len(listall)
		semua = listall
		jarak = 0
		jarak2 = 0
		for x in range(math.ceil(len(listall)/100)):
			if total >= 101:
				jarak2 += 100
				await client.delete_messages(message.chat.id, message_ids=semua[jarak:jarak2])
				jarak += 100
				total -= 100
			else:
				jarak2 += total
				await client.delete_messages(message.chat.id, message_ids=semua[jarak:jarak2])
				jarak += total
				total -= total
	else:
		await client.delete_messages(message.chat.id, message_ids=listall)


@app.on_message(Filters.user("self") & Filters.command(["purgeme"], Command))
async def purge_myself(client, message):
	if len(message.text.split()) >= 2 and message.text.split()[1].isdigit():
		target = int(message.text.split()[1])
	else:
		await message.edit("Give me a number for a range!")
	get_msg = await client.get_history(message.chat.id)
	listall = []
	counter = 0
	for x in get_msg:
		if counter == target+1:
			break
		if x.from_user.id == int(Owner):
			listall.append(x.message_id)
			counter += 1
	if len(listall) >= 101:
		total = len(listall)
		semua = listall
		jarak = 0
		jarak2 = 0
		for x in range(math.ceil(len(listall)/100)):
			if total >= 101:
				jarak2 += 100
				await client.delete_messages(message.chat.id, message_ids=semua[jarak:jarak2])
				jarak += 100
				total -= 100
			else:
				jarak2 += total
				await client.delete_messages(message.chat.id, message_ids=semua[jarak:jarak2])
				jarak += total
				total -= total
	else:
		await client.delete_messages(message.chat.id, message_ids=listall)
