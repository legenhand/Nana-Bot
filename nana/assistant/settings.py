from platform import python_version

import heroku3
from pyrogram import Filters, InlineKeyboardButton, InlineKeyboardMarkup, errors
from .theme.theme import get_theme
from nana import AdminSettings, setbot, app, USERBOT_VERSION, ASSISTANT_VERSION, DB_AVAILABLE, HEROKU_API, Owner
from nana.__main__ import reload_userbot, restart_all
from nana.assistant.__main__ import dynamic_data_filter


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
                   [InlineKeyboardButton("Set Sticker", callback_data="setsticker")]]
    if HEROKU_API:
        list_button.append([InlineKeyboardButton("Heroku Config Vars", callback_data="heroku_vars")])
        list_button.append([InlineKeyboardButton("Restart Heroku app", callback_data="restart_heroku")])
        list_button.append([InlineKeyboardButton("Change Repo Source", callback_data="change_repo")])
    return InlineKeyboardMarkup(list_button)


@setbot.on_message(Filters.user(AdminSettings) & Filters.command(["settings"]) & Filters.private)
async def settings(_client, message):
    text = await get_text_settings()
    button = await get_button_settings()
    img = await get_theme("Nana-Official", "settings")
    await setbot.send_photo(Owner, img, caption=text, reply_markup=button)


@setbot.on_callback_query(dynamic_data_filter("toggle_startbot"))
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


@setbot.on_callback_query(dynamic_data_filter("restart_bot"))
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


@setbot.on_callback_query(dynamic_data_filter("restart_heroku"))
async def reboot_heroku(client, query):
    text = await get_text_settings()
    button = await get_button_settings()
    if HEROKU_API is not None:
        text += "\nPlease wait..."
        try:
            await query.message.edit_text(text, reply_markup=button)
        except errors.exceptions.bad_request_400.MessageNotModified:
            pass
        await client.answer_callback_query(query.id, "Please wait for Heroku App restarting...")
        heroku = heroku3.from_key(HEROKU_API)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            heroku_app = heroku_applications[0]
            heroku_app.restart()
        else:
            text += "No heroku application found, but a key given? 😕"
    try:
        await query.message.edit_text(text, reply_markup=button)
    except errors.exceptions.bad_request_400.MessageNotModified:
        pass
    await client.answer_callback_query(query.id, "No heroku application found, but a key given?")


@setbot.on_callback_query(dynamic_data_filter("heroku_vars"))
async def vars_heroku(_client, query):
    text = "**⚙️ Welcome to Heroku Vars Settings!**\n" \
           "`Setting your heroku config vars here!`\n"
    list_button = [[InlineKeyboardButton("⬅ back️", callback_data="back"),
                    InlineKeyboardButton("➕  add️", callback_data="add_vars")]]
    if HEROKU_API:
        heroku = heroku3.from_key(HEROKU_API)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            app = heroku_applications[0]
            config = app.config()
            # if config["api_id"]:
            #     list_button.insert(0, [InlineKeyboardButton("api_id✅", callback_data="api_id")])
            # else:
            #     list_button.insert(0, [InlineKeyboardButton("api_id🚫", callback_data="api_id")])
            configdict = config.to_dict()
            for x, _ in configdict.items():
                list_button.insert(0, [InlineKeyboardButton("{}✅".format(x), callback_data="tes")])
    button = InlineKeyboardMarkup(list_button)
    await query.message.edit_text(text, reply_markup=button)

# Back button

@setbot.on_callback_query(dynamic_data_filter("back"))
async def back(_client, message):
    text = await get_text_settings()
    button = await get_button_settings()
    img = await get_theme("Nana-Official", "settings")
    await setbot.send_photo(Owner, img, caption=text, reply_markup=button)
