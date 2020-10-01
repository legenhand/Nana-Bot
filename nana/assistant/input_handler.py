import heroku3
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from nana import AdminSettings, setbot, Owner, HEROKU_API, DB_AVAILABLE
from nana.assistant.database.custom_theme_db import add_custom_theme
from nana.assistant.database.stickers_db import set_stanim_set, set_sticker_set
from nana.assistant.settings import get_text_settings, get_button_settings
from nana.assistant.theme.theme_helper import get_theme

temp_input = False
theme_format = []
temp_query = {}
temp_vars = []
TEMP_KEYBOARD = []
USER_SET = {}


@setbot.on_message(filters.user(AdminSettings))
async def theme_input_handlers(client, message):
    global temp_input, theme_format, temp_query, temp_vars, USER_SET, TEMP_KEYBOARD
    if temp_input:
        text = "**⚙️Add Theme **\n"
        if len(theme_format) >= 1:
            try:
                cap = "Image has been set!"
                await setbot.send_photo(Owner, message.text, caption=cap)
                theme_format.append(message.text)
            except:
                text += "**Wrong URL image !** \n"
        else:
            theme_format.append(message.text)

        if len(theme_format) == 1:
            text += f"Set URL image for welcome image \n"
        elif len(theme_format) == 2:
            text += f"Set URL image for start image \n"
        elif len(theme_format) == 3:
            text += f"Set URL image for settings image \n"
        elif len(theme_format) == 4:
            text += f"Set URL image for stats image \n"
        elif len(theme_format) == 5:
            text += f"Custom Theme has successfully added \n"
            temp_input = False
            await add_custom_theme(theme_format[0], theme_format[1], theme_format[2], theme_format[3], theme_format[4])
            theme_format = []
        list_button = [[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]
        button = InlineKeyboardMarkup(list_button)
        await client.send_message(Owner, text, reply_markup=button)
    elif len(temp_vars) >= 1:
        temp_vars.append(message.text)
        text = "**⚙️Add heroku config vars **\n"
        if len(temp_vars) == 2:
            text += "`Send Value `"
            list_button = [[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]
            button = InlineKeyboardMarkup(list_button)
            await client.send_message(Owner, text, reply_markup=button)
        if len(temp_vars) == 3:
            await config_vars(temp_vars[1], temp_vars[2])
            text += "`Successfully added config vars! `"
            await client.send_message(Owner, text)
            temp_vars = []
    elif message.from_user and message.from_user.id in list(USER_SET):
        if not DB_AVAILABLE:
            await message.edit("Your database is not avaiable!")
            return
        if message.text in TEMP_KEYBOARD:
            await client.delete_messages(message.chat.id, USER_SET[message.from_user.id])
            print(USER_SET)
            if USER_SET["type"] == 2:
                set_sticker_set(message.from_user.id, message.text)
            elif USER_SET["type"] == 1:
                set_stanim_set(message.from_user.id, message.text)
            status = "Ok, sticker was set to `{}`".format(message.text)
            TEMP_KEYBOARD = []
            USER_SET = {}
        else:
            status = "Invalid pack selected."
            TEMP_KEYBOARD = []
            USER_SET = {}
        text = await get_text_settings()
        text += "\n{}".format(status)
        button = await get_button_settings()
        img = await get_theme("settings")
        await setbot.send_photo(Owner,
                                img,
                                caption=text, reply_markup=button)


@setbot.on_callback_query(filters.regex("^cancel"))
async def cancel_input(client, query):
    global temp_input, theme_format, temp_vars
    temp_input = False
    theme_format = []
    temp_vars = []
    await client.answer_callback_query(query.id, "Operation Canceled!")
    await query.message.delete()


async def config_vars(name, value):
    if HEROKU_API:
        heroku = heroku3.from_key(HEROKU_API)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            app = heroku_applications[0]
            config = app.config()
            config[name] = value
