import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from nana import app, setbot, Command, Owner, BotUsername, DB_AVAILABLE, AdminSettings, OwnerName, PM_PERMIT
from nana.helpers.parser import mention_markdown

if DB_AVAILABLE:
    from nana.modules.database.pm_db import set_whitelist, get_whitelist, set_req, get_req, del_whitelist

welc_txt = f"""
Hello, I'm {OwnerName}'s Userbot.
Try contacting me by pressing buttons down below
"""


NOTIFY_ID = Owner
BLACKLIST = ["hack", "fuck", "bitch", "pubg", "sex"]


@app.on_message(~filters.me & filters.private & ~filters.bot)
async def pm_block(client, message):
    if not PM_PERMIT:
        return
    if not get_whitelist(message.chat.id):
        await client.read_history(message.chat.id)
        if message.text:
            for x in message.text.lower().split():
                if x in BLACKLIST:
                    await client.send_sticker(message.chat.id,
                                              sticker='CAADAgAD1QQAAp7kTAry1JrL3zVXSxYE'
                                              )
                    await message.reply("Naah im blocking you and reporting you to SpamWatch,\nwith that being said fuck you too OwO")
                    await client.block_user(message.chat.id)
                    return
        if not get_req(message.chat.id):
            x = await client.get_inline_bot_results(BotUsername, "engine_pm")
        else:
            x = await client.get_inline_bot_results(BotUsername, "engine_pm")
        await client.send_inline_bot_result(message.chat.id, query_id=x.query_id,
                                            result_id=x.results[0].id, hide_via=True
                                            )


@app.on_message(filters.me & filters.command("approve", Command) & filters.private)
async def approve_pm(_client, message):
    set_whitelist(message.chat.id, True)
    await message.edit("**PM permission was approved!**")


@app.on_message(filters.me & filters.command(["revoke", "disapprove"], Command) & filters.private)
async def revoke_pm_block(_client, message):
    del_whitelist(message.chat.id)
    await message.edit("**PM permission was revoked!**")


def pm_button_callback(_, __, query):
    if re.match("engine_pm", query.data):
        return True


pm_filter = filters.create(pm_button_callback)


@setbot.on_callback_query(pm_filter)
async def pm_button(client, query):
    print(query)
    if not PM_PERMIT:
        return
    if query.from_user.id in AdminSettings and not re.match("engine_pm_apr", query.data) and not re.match("engine_pm_blk", query.data):
        await client.answer_callback_query(query.id, "No, you can't click by yourself", show_alert=False)
        return
    if re.match("engine_pm_block", query.data):
        await app.send_sticker(query.from_user.id, sticker='CAADAgAD1QQAAp7kTAry1JrL3zVXSxYE')
        await setbot.edit_inline_text(query.from_user.id, "Sorry, No cash.\nAlso you are getting reported to **SpamWatch**, OwO")
        await app.block_user(query.from_user.id)
    elif re.match("engine_pm_nope", query.data):
        await setbot.edit_inline_text(query.inline_message_id, "👍")
        await app.send_message(query.from_user.id, "Hello, please wait for a reply from my master, thank you")
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Approve",
                                                            callback_data=f"engine_pm_apr-{query.from_user.id}"),
                                        InlineKeyboardButton("Block",
                                                            callback_data=f"engine_pm_blk-{query.from_user.id}")]])
        pm_bot_mention = mention_markdown(query.from_user.id, query.from_user.first_name)
        pm_bot_message = f"[{OwnerName}](tg://user?id={Owner}), {pm_bot_mention} want to contact you~"
        await setbot.send_message(NOTIFY_ID, pm_bot_message,reply_markup=buttons)
        set_req(query.from_user.id, True)
    elif re.match("engine_pm_report", query.data):
        await setbot.edit_inline_text(query.inline_message_id, "👍")
        await app.send_message(query.from_user.id, "Hello, if you want to report any bugs, please vist in @NanaBotSupport")
    elif re.match("engine_pm_none", query.data):
        await setbot.edit_inline_text(query.inline_message_id, "👍")
        await app.send_message(query.from_user.id, "Alright then,\nIf you want anything from me, please contact my again. Thank you")
    elif re.match("engine_pm_apr", query.data):
        target = query.data.split("-")[1]
        await query.message.edit_text(f"[Approved for PM]({target})")
        await app.send_message(target, "Hello, this is **Nana**, my master approved you to PM.")
        set_whitelist(int(target), True)
    elif re.match(r"engine_pm_blk", query.data):
        target = query.data.split("-")[1]
        await query.message.edit_text("That user was blocked ~")
        await app.send_message(target, "Hello, this is **Nana**, my master has decide to block you.\nSorry for this!")
        await app.block_user(target)
    else:
        await setbot.edit_inline_text(query.inline_message_id, "🙆‍")
