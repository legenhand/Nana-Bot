from pyrogram import Filters, InlineKeyboardButton, InlineKeyboardMarkup
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
    await set_name_theme_set(Owner, name, False)
    text = "**⚙️Theme Configuration **\n" \
           f"Theme Changed To `{name}`\n"

    await query.message.edit_text(text)


@setbot.on_callback_query(Filters.regex("^cthm"))
async def chg_custom_theme(_client, query):
    code_theme = query.data
    await set_name_theme_set(Owner, code_theme, True)
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
    list_button = [[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]
    button = InlineKeyboardMarkup(list_button)
    await client.send_message(Owner, text, reply_markup=button)


@setbot.on_callback_query(Filters.regex("^cancel"))
async def addtheme(client, query):
    global temp_input, theme_format
    if temp_input:
        temp_input = False
        theme_format = []
        await client.answer_callback_query(query.id, "Operation Canceled!")
        await query.message.delete()


@setbot.on_message(Filters.user(AdminSettings))
async def theme_input_handlers(client, message):
    global temp_input, theme_format, temp_query, temp_client
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


