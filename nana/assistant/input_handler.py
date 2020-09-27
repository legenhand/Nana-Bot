import heroku3
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from nana import AdminSettings, setbot, Owner, HEROKU_API
from nana.assistant.database.custom_theme_db import add_custom_theme

temp_input = False
theme_format = []
temp_query = {}
temp_vars = []


@setbot.on_message(filters.user(AdminSettings))
async def theme_input_handlers(client, message):
    global temp_input, theme_format, temp_query, temp_vars
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
