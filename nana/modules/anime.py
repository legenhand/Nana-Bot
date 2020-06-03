import datetime
import html
import textwrap
import bs4
import jikanpy
import requests
import asyncio

from pyrogram import Filters

from nana.helpers.PyroHelpers import ReplyCheck
from nana import app, Command




# upcomming
jikan = jikanpy.jikan.Jikan()
upcoming = jikan.top('anime', page=1, subtype="upcoming")

upcoming_list = [entry['title'] for entry in upcoming['top']]
upcoming_message = ""

for entry_num in range(len(upcoming_list)):
    if entry_num == 10:
        break
    upcoming_message += f"{entry_num + 1}. {upcoming_list[entry_num]}\n"

await message.edit(upcoming_message)

def replace_text(text):
        return text.replace("\"", "").replace("\\r", "").replace("\\n", "\n").replace(
            "\\", "")