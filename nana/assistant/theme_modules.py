from pyrogram import Filters
from nana import setbot, Owner, AdminSettings
from .database.custom_theme_db import add_custom_theme
from .database.theme_db import set_name_theme_set
from .theme.theme_helper import theme_list, name_theme

temp_input = False
theme_format = []
temp_query = {}
temp_client = ""


@setbot.on_callback_query(Filters.regex("^theme"))
async def chgtheme(_client, query):
    text = "**⚙ Theme Configuration **\n" \
           "`Change Your Nana Theme Here! `\n"

    button = await theme_list()
    await query.message.edit_text(text, reply_markup=button)


@setbot.on_callback_query(Filters.regex("^thm"))
async def chgtheme(_client, query):
    code_theme = query.data[4:]
    name = await name_theme(code_theme)
    await set_name_theme_set(Owner, name)
    text = "**⚙️Theme Configuration **\n" \
           f"Theme Changed To `{name}`\n"

    await query.message.edit_text(text)


@setbot.on_callback_query(Filters.regex("^cthm"))
async def chg_custom_theme(_client, query):
    code_theme = query.data
    await set_name_theme_set(Owner, code_theme)
    text = "**⚙️Theme Configuration **\n" \
           f"Theme Changed !\n"

    await query.message.edit_text(text)


@setbot.on_callback_query(Filters.regex("^addtheme"))
async def addtheme(client, query):
    await query.message.delete()
    global temp_input
    temp_input = True
    text = "**⚙️Add Theme **\n" \
           f"Set Name theme \n"
    await client.send_message(Owner, text)


@setbot.on_message(Filters.user(AdminSettings))
async def theme_input_handlers(client, message):
    global temp_input, theme_format, temp_query, temp_client
    if temp_input:
        theme_format.append(message.text)
        print(theme_format)
        if len(theme_format) == 1:
            text = "**⚙️Add Theme **\n" \
                   f"Set URL image for welcome image \n"
        elif len(theme_format) == 2:
            text = "**⚙️Add Theme **\n" \
                   f"Set URL image for start image \n"
        elif len(theme_format) == 3:
            text = "**⚙️Add Theme **\n" \
                   f"Set URL image for settings image \n"
        elif len(theme_format) == 4:
            text = "**⚙️Add Theme **\n" \
                   f"Set URL image for stats image \n"
        elif len(theme_format) == 5:
            text = "**⚙️Add Theme **\n" \
                   f"Custom Theme has successfully added \n"
            temp_input = False
            await add_custom_theme(theme_format[0], theme_format[1], theme_format[2], theme_format[3], theme_format[4])
            theme_format = []

        await client.send_message(Owner, text)

# TODO : Added User Theme Customization
