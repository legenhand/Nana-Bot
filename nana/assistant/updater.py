import random

from git import Repo
from git.exc import GitCommandError, NoSuchPathError, InvalidGitRepositoryError
from pyrogram import Filters, InlineKeyboardMarkup, InlineKeyboardButton

from nana import setbot, Owner, USERBOT_VERSION, ASSISTANT_VERSION, log, OFFICIAL_BRANCH, \
    REPOSITORY, RANDOM_STICKERS, REMINDER_UPDATE, TEST_DEVELOP, HEROKU_API
from nana.__main__ import restart_all, loop


async def gen_chlog(repo, diff):
    changelog = ""
    d_form = "%H:%M - %d/%m/%y"
    try:
        for cl in repo.iter_commits(diff):
            changelog += f'• [{cl.committed_datetime.strftime(d_form)}]: {cl.summary} <{cl.author}>\n'
    except GitCommandError:
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
    except NoSuchPathError as error:
        log.warning(f"Check update failed!\nDirectory {error} is not found!")
        return
    except InvalidGitRepositoryError as error:
        log.warning(f"Check update failed!\nDirectory {error} does not seems to be a git repository")
        return
    except GitCommandError as error:
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
async def update_button(_client, query):
    await query.message.edit_text("Updating, please wait...")
    try:
        repo = Repo()
    except NoSuchPathError as error:
        log.warning(f"Check update failed!\nDirectory {error} is not found!")
        return
    except InvalidGitRepositoryError as error:
        log.warning(f"Check update failed!\nDirectory {error} does not seems to be a git repository")
        return
    except GitCommandError as error:
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
    if HEROKU_API is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_API)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            heroku_app = heroku_applications[0]
            heroku_git_url = heroku_app.git_url.replace(
                "https://",
                "https://api:" + HEROKU_API + "@"
            )
            if "heroku" in repo.remotes:
                remote = repo.remote("heroku")
                remote.set_url(heroku_git_url)
            else:
                remote = repo.create_remote("heroku", heroku_git_url)
            remote.push(refspec="HEAD:refs/heads/master")
        else:
            await query.reply("no heroku application found, but a key given? 😕 ")
        await query.reply("Build Unsuccess, Check heroku build log for more detail")
        return
    try:
        upstream.pull(brname)
        await query.message.edit_text('Successfully Updated!\nBot is restarting...')
    except GitCommandError:
        repo.git.reset('--hard')
        repo.git.clean('-fd', 'nana/modules/')
        repo.git.clean('-fd', 'nana/assistant/')
        repo.git.clean('-fd', 'nana/helpers/')
        await query.message.edit_text('Successfully Force Updated!\nBot is restarting...')
    await update_changelog(changelog)
    await restart_all()


if REMINDER_UPDATE and not TEST_DEVELOP:
    loop.create_task(update_checker())


async def starting_message():
    await setbot.send_message(Owner, "**Your Bot Ready to go!**\n\nSee /help for more information` 😉")


loop.create_task(starting_message())
