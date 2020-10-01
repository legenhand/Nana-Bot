import random
import re

from pyrogram import filters
from pyrogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

from nana import setbot, AdminSettings


def cat_callback(_, __, query):
    if re.match("cat_pic", query.data):
        return True

cat_create = filters.create(cat_callback)

def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

@setbot.on_callback_query(cat_create)
async def catpic_callback(client, query):
    if query.from_user.id in AdminSettings:
        image = f"https://d2ph5fj80uercy.cloudfront.net/0{random.randint(1, 6)}/cat{random.randint(0,4999)}.jpg"
        buttons = [[InlineKeyboardButton("Source", url="https://thiscatdoesnotexist.com/"), InlineKeyboardButton("Refresh", callback_data='cat_pic')]]
        await setbot.edit_inline_media(query.inline_message_id, InputMediaPhoto(media=image,
                                                                                caption='Hi I like you too >~<'),
                                       reply_markup=InlineKeyboardMarkup(buttons)
                                       )
    else:
        await client.answer_callback_query(query.id,
                                           "No, you are not allowed to do this",
                                           show_alert=False)