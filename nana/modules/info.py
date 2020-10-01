from datetime import datetime
from time import sleep

import spamwatch
from pyrogram import filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.raw import functions
from pyrogram.types import User

from nana import app, Command, sw_api, AdminSettings, edrep

__MODULE__ = "Whois"
__HELP__ = """
──「 **Whois** 」──
-> `info` `@username` or `user_id`
-> `info` "reply to a text"
To find information about a person.

"""




def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == 'recently':
        return "Recently"
    elif user.status == 'within_week':
        return "Within the last week"
    elif user.status == 'within_month':
        return "Within the last month"
    elif user.status == 'long_time_ago':
        return "A long time ago :("
    elif user.status == 'online':
        return "Currently Online"
    elif user.status == 'offline':
        return datetime.fromtimestamp(user.status.date).strftime("%a, %d %b %Y, %H:%M:%S")


async def GetCommon(client, get_user):
    common = await client.send(
        functions.messages.GetCommonChats(
            user_id=await client.resolve_peer(get_user),
            max_id=0,
            limit=0))
    return common


def ProfilePicUpdate(user_pic):
    return datetime.fromtimestamp(user_pic[0].date).strftime("%d.%m.%Y, %H:%M:%S")


@app.on_message(filters.user(AdminSettings) & filters.command("info", Command))
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        if message.reply_to_message.forward_from:
            get_user = message.reply_to_message.forward_from.id
        else:
            get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await edrep(message, text="I don't know that User.")
        sleep(2)
        await message.delete()
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    common = await GetCommon(client, user.id)

    if user:
        if sw_api:
            sw = spamwatch.Client(sw_api)
            status = sw.get_ban(user.id)
            if status == False:
                await edrep(message, text=f"""
**About [{user.first_name} {user.last_name if user.last_name else ''}](tg://user?id={user.id})**:
  - **UserID**: `{user.id}`
  - **Username**: {'@'+user.username if user.username else ''}
  - **Last Online**: `{LastOnline(user)}`
  - **Common Groups**: `{len(common.chats)}`
  - **Contact**: `{user.is_contact}`
**SpamWatch Banned** : `False`
                """,
                disable_web_page_preview=True)
            else:
                await edrep(message, text=f"""
**About [{user.first_name} {user.last_name if user.last_name else ''}](tg://user?id={user.id})**:
  - **UserID**: `{user.id}`
  - **Username**: {'@'+user.username if user.username else ''}
  - **Last Online**: `{LastOnline(user)}`
  - **Common Groups**: `{len(common.chats)}`
  - **Contact**: `{user.is_contact}`
**SpamWatch Banned** : `True`
  • **Reason**: `{status.reason}`
  • **Message**: `{status.message}`
                """,
                disable_web_page_preview=True)
            return
        else:
            await edrep(message, text=f"""
**About [{user.first_name} {user.last_name if user.last_name else ''}](tg://user?id={user.id})**:
  - **UserID**: `{user.id}`
  - **Username**: {'@'+user.username if user.username else ''}
  - **Last Online**: `{LastOnline(user)}`
  - **Common Groups**: `{len(common.chats)}`
  - **Contact**: `{user.is_contact}`
            """,
            disable_web_page_preview=True)