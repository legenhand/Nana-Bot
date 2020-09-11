from nana.helpers.aiohttp_helper import AioHttp
from nana.assistant.database.theme_db import get_name_theme_set
from nana import Owner
from pyrogram import InlineKeyboardButton, InlineKeyboardMarkup


async def get_theme(name, type):
    theme = await AioHttp().get_json('http://api.harumi.tech/theme')
    name = await get_name_theme_set(Owner)
    return theme[name][type]


async def theme_list():
    theme = await AioHttp().get_json('http://api.harumi.tech/theme')
    list_button = []
    print(theme["Nana-Official"]["theme-code"])
    for i in theme.items():
        call_code = theme[i]["theme-code"]
        print(i, call_code)
        list_button.append([InlineKeyboardButton(i, callback_data=call_code)])
    list_button.append([InlineKeyboardButton("⬅ back️", callback_data="back")])
    return InlineKeyboardMarkup(list_button)
