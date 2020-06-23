import re

from nana import app, setbot, Command, Owner, OwnerName, BotUsername, AdminSettings, DB_AVAILABLE, lydia_api, AdminSettings
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton

from nana.helpers.parser import mention_markdown

if DB_AVAILABLE:
	from nana.modules.database.pm_db import set_whitelist, get_whitelist, set_req, get_req, del_whitelist

async def get_welcome():
	me = await app.get_me()
	return f"""Hello, i am Nana, @{me.username}'s Userbot.
			Just say what do you want by this button 👇👍"""


NOTIFY_ID = AdminSettings[0]
BLACKLIST = ["hack", "fuck", "bitch"]

USER_IN_RESTRICT = []


@app.on_message(~Filters.user("self") & Filters.private & ~Filters.bot)
async def pm_block(client, message):
	if not get_whitelist(message.chat.id):
		await client.read_history(message.chat.id)
		if message.text:
			for x in message.text.lower().split():
				if x in BLACKLIST:
					# await message.reply("Fuck you too!")
					await client.block_user(message.chat.id)
					return
		from nana.modules.lydia import lydia_status
		print(get_req(message.chat.id))
		if not get_req(message.chat.id):
			result = await client.get_inline_bot_results(BotUsername, "engine_pm")
			result = await client.send_inline_bot_result(message.chat.id, query_id=result.query_id, result_id=result.results[0].id, hide_via=True)
		elif lydia_api and lydia_status:
			from .lydia import lydia_reply
			await lydia_reply(client, message)
		else:
			result = await client.get_inline_bot_results(BotUsername, "engine_pm")
			result = await client.send_inline_bot_result(message.chat.id, query_id=result.query_id, result_id=result.results[0].id, hide_via=True)

@app.on_message(Filters.me & Filters.command(["approvepm"], Command) & Filters.private)
async def approve_pm(_client, message):
	set_whitelist(message.chat.id, True)
	await message.edit("PM permission was approved!")

@app.on_message(Filters.me & Filters.command(["revokepm", "disapprovepm"], Command) & Filters.private)
async def revoke_pm_block(_client, message):
	del_whitelist(message.chat.id)
	await message.edit("PM permission was revoked!")

def pm_button_callback(_, query):
	if re.match(r"engine_pm", query.data):
		return True

pm_button_create = Filters.create(pm_button_callback)

@setbot.on_callback_query(pm_button_create)
async def pm_button(client, query):
	if query.from_user.id in AdminSettings and not re.match(r"engine_pm_apr", query.data) and not re.match(r"engine_pm_blk", query.data):
		await client.answer_callback_query(query.id, "No, you can't click by yourself", show_alert=False)
		return
	if re.match(r"engine_pm_block", query.data):
		await setbot.edit_inline_text(query.inline_message_id, "💩")
		# await app.send_message(query.from_user.id, "I dont share any hack or any illegal things, if you PM me for this, then you are retard and does not have a brain.\nContact your admin and ask that illegal things, not me\n\nGood bye you fucking retard!")
		await app.block_user(query.from_user.id)
	elif re.match(r"engine_pm_nope", query.data):
		await setbot.edit_inline_text(query.inline_message_id, "👍")
		await app.send_message(query.from_user.id, "Hello, please wait for a reply from my master\nI've notify my master to reply your PM, thank you")
		FromUser = mention_markdown(query.from_user.id, query.from_user.first_name)
		await setbot.send_message(NOTIFY_ID, "Hi [ {} ](tg://user?id={}), {} want to contact you~".format(OwnerName, Owner, FromUser), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Approve", callback_data="engine_pm_apr-{}".format(query.from_user.id)), InlineKeyboardButton("Block", callback_data="engine_pm_blk-{}".format(query.from_user.id))]]))
		set_req(query.from_user.id, True)
		from nana.modules.lydia import lydia_status
		if lydia_status:
			await app.send_message(query.from_user.id, "During the wait for permission from my master, why do not we have a little chat?")
	elif re.match(r"engine_pm_report", query.data):
		await setbot.edit_inline_text(query.inline_message_id, "👍")
		await app.send_message(query.from_user.id, "Hello, if you want to report any bugs for my bots, please report in @NanaBotSupport\nThank you")
	elif re.match(r"engine_pm_none", query.data):
		await setbot.edit_inline_text(query.inline_message_id, "👍")
		await app.send_message(query.from_user.id, "Alright then,\nIf you want anything from me, please contact my again. Thank you")
	elif re.match(r"engine_pm_donate", query.data):
		await setbot.edit_inline_text(query.inline_message_id, "❤️")
		await app.send_message(query.from_user.id, "Cool, thank you for donate me\nYou can select payment in here https://ayrahikari.github.io/donations.html\n\nIf you've donated me, please PM me again, thanks")
	elif re.match(r"engine_pm_apr", query.data):
		target = query.data.split("-")[1]
		await query.message.edit_text("[Approved for PM]({})".format(target))
		await app.send_message(target, "Hello, this is Nana, my master approved you to PM.")
		set_whitelist(int(target), True)
	elif re.match(r"engine_pm_blk", query.data):
		target = query.data.split("-")[1]
		await query.message.edit_text("That user was blocked~")
		await app.send_message(target, "Hello, this is Nana, my master has decide to block you.\nSorry for this!")
		await app.block_user(target)
	else:
		await setbot.edit_inline_text(query.inline_message_id, "🙆‍♀️")
