from platform import python_version

from pyrogram import filters, errors
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nana import setbot, app, USERBOT_VERSION, ASSISTANT_VERSION, DB_AVAILABLE, HEROKU_API, Owner
from nana.__main__ import reload_userbot, restart_all
from .theme.theme_helper import get_theme


async def is_userbot_run():
    try:
        return await app.get_me()
    except ConnectionError:
        return None


async def get_text_settings():
    me = await is_userbot_run()
    if not me:
        text = "-> Userbot: `Stopped (v{})`\n".format(USERBOT_VERSION)
    else:
        text = "-> Userbot: `Running (v{})`\n".format(USERBOT_VERSION)
    text += "-> Assistant: `Running (v{})`\n".format(ASSISTANT_VERSION)
    text += "-> Database: `{}`\n".format(DB_AVAILABLE)
    text += "-> Python: `{}`\n".format(python_version())
    return text


async def get_button_settings():
    me = await is_userbot_run()
    if me:
        toggle = "Stop Bot"
    else:
        toggle = "Start Bot"
    list_button = [[InlineKeyboardButton(toggle, callback_data="toggle_startbot"),
                    InlineKeyboardButton("Restart Bot", callback_data="restart_bot")],
                   [InlineKeyboardButton("Set Sticker", callback_data="setsticker")],
                   [InlineKeyboardButton("Set Theme", callback_data="theme")]]
    if HEROKU_API:
        list_button.append([InlineKeyboardButton("Heroku Config Vars", callback_data="heroku_vars")])
        list_button.append([InlineKeyboardButton("Restart Heroku app", callback_data="restart_heroku")])
        list_button.append([InlineKeyboardButton("Change Repo Source", callback_data="change_repo")])
    return InlineKeyboardMarkup(list_button)


@setbot.on_callback_query(filters.regex("^toggle_startbot"))
async def start_stop_bot(client, query):
    try:
        await app.stop()
    except ConnectionError:
        await reload_userbot()
        text = await get_text_settings()
        button = await get_button_settings()
        text += "\n✅ Bot was started!"
        try:
            await query.message.edit_text(text, reply_markup=button)
        except errors.exceptions.bad_request_400.MessageNotModified:
            pass
        await client.answer_callback_query(query.id, "Bot was started!")
        return
    text = await get_text_settings()
    button = await get_button_settings()
    text += "\n❎ Bot was stopped!"
    try:
        await query.message.edit_text(text, reply_markup=button)
    except errors.exceptions.bad_request_400.MessageNotModified:
        pass
    await client.answer_callback_query(query.id, "Bot was stopped!")


@setbot.on_callback_query(filters.regex("^restart_bot"))
async def reboot_bot(client, query):
    await restart_all()
    text = await get_text_settings()
    text += "\n✅ Bot was restarted!"
    button = await get_button_settings()
    try:
        await query.message.edit_text(text, reply_markup=button)
    except errors.exceptions.bad_request_400.MessageNotModified:
        pass
    await client.answer_callback_query(query.id, "Please wait for bot restarting...")

# Back button


@setbot.on_callback_query(filters.regex("^back"))
async def back(_client, message):
    text = await get_text_settings()
    button = await get_button_settings()
    img = await get_theme("settings")
    await setbot.send_photo(Owner, img, caption=text, reply_markup=button)

