
import time

from pyrogram import filters

from nana import setbot, AdminSettings, BotUsername, app, Command, OwnerUsername, StartTime
from nana.helpers.PyroHelpers import ReplyCheck


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
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


@setbot.on_callback_query(filters.regex("^alive_message"))
async def  alivemsg_callback(client, query):
    start_time = time.time()
    uptime = get_readable_time((time.time() - StartTime))
    reply_msg = f"{OwnerUsername}@nana-remix\n"
    reply_msg += "------------------\n"
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    reply_msg += f"Ping: {ping_time}ms\n"
    reply_msg += f"Userbot uptime: {uptime}"
    await client.answer_callback_query(query.id, reply_msg, show_alert=True)


@app.on_message(filters.user(AdminSettings) & filters.command("alive", Command))
async def google_search(client, message):
    x = await client.get_inline_bot_results(f"{BotUsername}", "alive")
    await message.delete()
    await client.send_inline_bot_result(chat_id=message.chat.id,
                                        query_id=x.query_id,
                                        result_id=x.results[0].id,
                                        reply_to_message_id=ReplyCheck(message),
                                        hide_via=True)