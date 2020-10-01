import heroku3
from pyrogram import errors, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nana import setbot, HEROKU_API
from nana.assistant.input_handler import temp_vars
from nana.assistant.settings import get_text_settings, get_button_settings


@setbot.on_callback_query(filters.regex("^restart_heroku"))
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


@setbot.on_callback_query(filters.regex("^heroku_vars"))
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


@setbot.on_callback_query(filters.regex("^add_vars"))
async def addvars(client, query):
    temp_vars.append(True)
    await query.message.edit_text("Send Name Variable :")


