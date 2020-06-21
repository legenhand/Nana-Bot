import sys
import traceback
import random
from uuid import uuid4

from pyrogram import InlineQueryResultArticle
from pyrogram import errors, InlineKeyboardMarkup, InputTextMessageContent, InlineKeyboardButton

from nana import setbot, Owner, OwnerName, DB_AVAILABLE
from nana.helpers.msg_types import Types
from nana.helpers.string import parse_button, build_keyboard
from nana.modules.pm import welc_txt
from nana.modules.stylish import text_style_generator, formatting_text_inline, CHAR_OVER, CHAR_UNDER, CHAR_STRIKE, \
	CHAR_POINTS, upsidedown_text_inline, smallcaps, superscript, subscript, wide, bubbles, bubblesblack, smothtext
if DB_AVAILABLE:
	from nana.modules.database import notes_db

# TODO: Add more inline query
# TODO: Wait for pyro update to add more inline query
GET_FORMAT = {
	Types.TEXT.value: InlineQueryResultArticle,
	# Types.DOCUMENT.value: InlineQueryResultDocument,
	# Types.PHOTO.value: InlineQueryResultPhoto,
	# Types.VIDEO.value: InlineQueryResultVideo,
	# Types.STICKER.value: InlineQueryResultCachedSticker,
	# Types.AUDIO.value: InlineQueryResultAudio,
	# Types.VOICE.value: InlineQueryResultVoice,
	# Types.VIDEO_NOTE.value: app.send_video_note,
	# Types.ANIMATION.value: InlineQueryResultGif,
	# Types.ANIMATED_STICKER.value: InlineQueryResultCachedSticker,
	# Types.CONTACT: InlineQueryResultContact
}


@setbot.on_inline_query()
async def inline_query_handler(client, query):
	string = query.query.lower()
	answers = []

	if query.from_user.id != Owner:
		await client.answer_inline_query(query.id,
										results=answers,
										switch_pm_text="Sorry, this bot only for {}".format(OwnerName),
										switch_pm_parameter="createown"
									)
		return

	if string == "":
		await client.answer_inline_query(query.id,
										results=answers,
										switch_pm_text="Need help? Click here",
										switch_pm_parameter="help_inline"
									)
		return

	# Notes
	if string.split()[0] == "#note":
		if not DB_AVAILABLE:
			await client.answer_inline_query(query.id,
											results=answers,
											switch_pm_text="Your database isn't avaiable!",
											switch_pm_parameter="help_inline"
										)
			return
		if len(string.split()) == 1:
			allnotes = notes_db.get_all_selfnotes_inline(query.from_user.id)
			if not allnotes:
				await client.answer_inline_query(query.id,
												results=answers,
												switch_pm_text="You dont have any notes!",
												switch_pm_parameter="help_inline"
											)
				return
			if len(list(allnotes)) >= 30:
				rng = 30
			else:
				rng = len(list(allnotes))
			for x in range(rng):
				note = allnotes[list(allnotes)[x]]
				noteval = note["value"]
				notetype = note["type"]
				# notefile = note["file"]
				if notetype != Types.TEXT:
					continue
				note, button = parse_button(noteval)
				button = build_keyboard(button)
				answers.append(InlineQueryResultArticle(
					title="Note #{}".format(list(allnotes)[x]),
					description=note,
					input_message_content=InputTextMessageContent(note),
					reply_markup=InlineKeyboardMarkup(button)))
			await client.answer_inline_query(query.id,
											results=answers,
											switch_pm_text="Yourself notes",
											switch_pm_parameter="help_inline"
										)
			return
		q = string.split(None, 1)
		notetag = q[1]
		noteval = notes_db.get_selfnote(query.from_user.id, notetag)
		if not noteval:
			await client.answer_inline_query(query.id,
											results=answers,
											switch_pm_text="Note not found!",
											switch_pm_parameter="help_inline"
										)
			return
		note, button = parse_button(noteval.get('value'))
		button = build_keyboard(button)
		answers.append(InlineQueryResultArticle(
			title="Note #{}".format(notetag),
			description=note,
			input_message_content=InputTextMessageContent(note),
			reply_markup=InlineKeyboardMarkup(button)))
		try:
			await client.answer_inline_query(query.id,
											results=answers,
											cache_time=5
										)
		except errors.exceptions.bad_request_400.MessageEmpty:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			log_errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
			button = InlineKeyboardMarkup([[InlineKeyboardButton("🐞 Report bugs", callback_data="report_errors")]])
			text = "An error has accured!\n\n```{}```\n".format("".join(log_errors))
			await setbot.send_message(Owner, text, reply_markup=button)
			return

	# Stylish converter

	elif string.split()[0] == "stylish":
		if len(string.split()) == 1:
			await client.answer_inline_query(query.id,
											results=answers,
											switch_pm_text="Insert any text to convert it!",
											switch_pm_parameter="help_inline"
										)
			return
		text = string.split(None, 1)[1]
		upside = upsidedown_text_inline(text)
		answers.append(InlineQueryResultArticle(
			title=upside,
			description="Upside-down Text",
			input_message_content=InputTextMessageContent(upside)))
		over = text_style_generator(text, CHAR_OVER)
		answers.append(InlineQueryResultArticle(
			title=over,
			description="Overline Text",
			input_message_content=InputTextMessageContent(over)))
		under = text_style_generator(text, CHAR_UNDER)
		answers.append(InlineQueryResultArticle(
			title=under,
			description="Underline Text",
			input_message_content=InputTextMessageContent(under)))
		strike = text_style_generator(text, CHAR_STRIKE)
		answers.append(InlineQueryResultArticle(
			title=strike,
			description="Strike Text",
			input_message_content=InputTextMessageContent(strike)))
		points = text_style_generator(text, CHAR_POINTS)
		answers.append(InlineQueryResultArticle(
			title=points,
			description="Points Text",
			input_message_content=InputTextMessageContent(points)))
		smallcaps_conv = formatting_text_inline(text, smallcaps)
		answers.append(InlineQueryResultArticle(
			title=smallcaps_conv,
			description="Smallcaps Text",
			input_message_content=InputTextMessageContent(smallcaps_conv)))
		super_script = formatting_text_inline(text, superscript)
		answers.append(InlineQueryResultArticle(
			title=super_script,
			description="Superscript Text",
			input_message_content=InputTextMessageContent(super_script)))
		sub_script = formatting_text_inline(text, subscript)
		answers.append(InlineQueryResultArticle(
			title=sub_script,
			description="Subscript Text",
			input_message_content=InputTextMessageContent(sub_script)))
		wide_text = formatting_text_inline(text, wide)
		answers.append(InlineQueryResultArticle(
			title=wide_text,
			description="Wide Text",
			input_message_content=InputTextMessageContent(wide_text)))
		bubbles_text = formatting_text_inline(text, bubbles)
		answers.append(InlineQueryResultArticle(
			title=bubbles_text,
			description="Bubbles Text",
			input_message_content=InputTextMessageContent(bubbles_text)))
		bubblesblack_text = formatting_text_inline(text, bubblesblack)
		answers.append(InlineQueryResultArticle(
			title=bubblesblack_text,
			description="Bubbles Black Text",
			input_message_content=InputTextMessageContent(bubblesblack_text)))
		smoth_text = formatting_text_inline(text, smothtext)
		answers.append(InlineQueryResultArticle(
			title=smoth_text,
			description="Smoth Text",
			input_message_content=InputTextMessageContent(smoth_text)))
		await client.answer_inline_query(query.id,
										results=answers,
										switch_pm_text="Converted to stylish text",
										switch_pm_parameter="help_inline"
									)
		return

	elif string.split()[0] == "engine_pm":
		# PM_BTN = []
		button = [[InlineKeyboardButton("To Scam", callback_data="engine_pm_block")],
		[InlineKeyboardButton("I want to contact you", callback_data="engine_pm_nope")],
		[InlineKeyboardButton("I want to report something", callback_data="engine_pm_report")],
		[InlineKeyboardButton("Nope, never mind", callback_data="engine_pm_none")]]
		random.shuffle(button)
		answers.append(InlineQueryResultArticle(
			id=uuid4(),
			title="Engine pm",
			description="Filter pm",
			input_message_content=InputTextMessageContent(welc_txt),
			reply_markup=InlineKeyboardMarkup(button)))
		await client.answer_inline_query(query.id,
		results=answers,
			cache_time=0
		)
	