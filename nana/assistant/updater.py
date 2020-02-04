import os, time, html, random
import asyncio

from nana import app, setbot, Owner, AdminSettings, USERBOT_VERSION, ASSISTANT_VERSION, log, OFFICIAL_BRANCH, REPOSITORY, RANDOM_STICKERS, REMINDER_UPDATE, TEST_DEVELOP
from __main__ import restart_all, loop
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton, errors

from git import Repo, exc



async def gen_chlog(repo, diff):
	changelog = ""
	d_form = "%H:%M - %d/%m/%y"
	try:
		for cl in repo.iter_commits(diff):
			changelog += f'• [{cl.committed_datetime.strftime(d_form)}]: {cl.summary} <{cl.author}>\n'
	except exc.GitCommandError:
		changelog = None
	return changelog

async def update_changelog(changelog):
	await setbot.send_sticker(Owner, random.choice(RANDOM_STICKERS))
	text = "**Update successfully!**\n"
	text += f"🎉 Welcome to Nana Bot v{USERBOT_VERSION} & Assistant v{ASSISTANT_VERSION}\n"
	text += "\n──「 **Update changelogs** 」──\n"
	text += changelog
	await setbot.send_message(Owner, text)


async def update_checker():
	try:
		repo = Repo()
	except exc.NoSuchPathError as error:
		log.warning(f"Check update failed!\nDirectory {error} is not found!")
		return
	except exc.InvalidGitRepositoryError as error:
		log.warning(f"Check update failed!\nDirectory {error} does not seems to be a git repository")
		return
	except exc.GitCommandError as error:
		log.warning(f"Check update failed!\n{error}")
		return

	brname = repo.active_branch.name
	if brname not in OFFICIAL_BRANCH:
		return

	try:
		repo.create_remote('upstream', REPOSITORY)
	except BaseException:
		pass

	upstream = repo.remote('upstream')
	upstream.fetch(brname)
	changelog = await gen_chlog(repo, f'HEAD..upstream/{brname}')

	if not changelog:
		log.info(f'Nana is up-to-date with branch {brname}')
		return

	log.warning(f'New UPDATE available for [{brname}]!')

	text = f"**New UPDATE available for [{brname}]!**\n\n"
	text += f"**CHANGELOG:**\n`{changelog}`"
	button = InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Update Now!", callback_data="update_now")]])
	await setbot.send_message(Owner, text, reply_markup=button, parse_mode="markdown")

# For callback query button
def dynamic_data_filter(data):
	return Filters.create(
		lambda flt, query: flt.data == query.data,
		data=data  # "data" kwarg is accessed with "flt.data" above
	)

@setbot.on_callback_query(dynamic_data_filter("update_now"))
async def update_button(client, query):
	await query.message.edit_text("Updating, please wait...")
	try:
		repo = Repo()
	except exc.NoSuchPathError as error:
		log.warning(f"Check update failed!\nDirectory {error} is not found!")
		return
	except exc.InvalidGitRepositoryError as error:
		log.warning(f"Check update failed!\nDirectory {error} does not seems to be a git repository")
		return
	except exc.GitCommandError as error:
		log.warning(f"Check update failed!\n{error}")
		return

	brname = repo.active_branch.name
	if brname not in OFFICIAL_BRANCH:
		return

	try:
		repo.create_remote('upstream', REPOSITORY)
	except BaseException:
		pass

	upstream = repo.remote('upstream')
	upstream.fetch(brname)
	changelog = await gen_chlog(repo, f'HEAD..upstream/{brname}')

	try:
		upstream.pull(brname)
		await query.message.edit_text('Successfully Updated!\nBot is restarting...')
	except exc.GitCommandError:
		repo.git.reset('--hard')
		repo.git.clean('-fd', 'nana/modules/')
		repo.git.clean('-fd', 'nana/assistant/')
		repo.git.clean('-fd', 'nana/helpers/')
		await query.message.edit_text('Successfully Force Updated!\nBot is restarting...')
	await update_changelog(changelog)
	await restart_all()

if REMINDER_UPDATE and not TEST_DEVELOP:
	loop.create_task(update_checker())
