import requests
from typing import List
import time
from asyncio import sleep

from nana import app, Owner, Command, StartTime
from pyrogram import Filters

sites_list = {
    "Telegram": "https://api.telegram.org",
}


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def ping_func(to_ping: List[str]) -> List[str]:
    ping_result = []

    for each_ping in to_ping:

        start_time = time.time()
        site_to_ping = sites_list[each_ping]
        r = requests.get(site_to_ping)
        end_time = time.time()
        ping_time = str(round((end_time - start_time), 2)) + "s"

        pinged_site = f"<b>{each_ping}</b>"

        ping_text = f"{pinged_site}: <code>{ping_time}</code>"
        ping_result.append(ping_text)

    return ping_result


@app.on_message(Filters.user(Owner) & Filters.command(["ping"], Command))
async def ping(client, message):
    telegram_ping = ping_func(["Telegram"])[0].split(": ", 1)[1]
    uptime = get_readable_time((time.time() - StartTime))
    reply_msg = (
        f"<b>Time Taken:</b> <code>{telegram_ping}</code>\n<b>Userbot uptime:</b> <code>{uptime}</code>")
    await message.delete()
    await client.send_message(message.chat.id, reply_msg, parse_mode="html")
    await sleep(5.0)
    await message.delete()
