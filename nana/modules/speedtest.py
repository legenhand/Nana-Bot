import re

import speedtest
from pyrogram import filters

from nana import setbot, AdminSettings, BotUsername, app, Command
from nana.helpers.PyroHelpers import ReplyCheck


def speedtest_callback(_, __, query):
    if re.match("speedtest", query.data):
        return True

speedtest_create = filters.create(speedtest_callback)

def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

@setbot.on_callback_query(speedtest_create)
async def speedtestxyz_callback(client, query):
    if query.from_user.id in AdminSettings:
        await setbot.edit_inline_text(query.inline_message_id,'Runing a speedtest....')
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = '**SpeedTest Results:**'
        if query.data == 'speedtest_image':
            speedtest_image = speed.results.share()
            replym = f"**[SpeedTest Results:]({speedtest_image})**"
            await setbot.edit_inline_text(query.inline_message_id, replym, parse_mode="markdown")

        elif query.data == 'speedtest_text':
            result = speed.results.dict()
            replymsg += f"\n - **ISP:** `{result['client']['isp']}`"
            replymsg += f"\n - **Download:** `{speed_convert(result['download'])}`"
            replymsg += f"\n - **Upload:** `{speed_convert(result['upload'])}`"
            replymsg += f"\n - **Ping:** `{result['ping']}`"
            await setbot.edit_inline_text(query.inline_message_id, replymsg, parse_mode="markdown")
    else:
        await client.answer_callback_query(query.id, "No, you are not allowed to do this", show_alert=False)


@app.on_message(filters.user(AdminSettings) & filters.command("speedtest", Command))
async def google_search(client, message):
    x = await client.get_inline_bot_results(f"{BotUsername}", f"speedtest")
    await message.delete()
    await client.send_inline_bot_result(chat_id=message.chat.id,
                                        query_id=x.query_id,
                                        result_id=x.results[0].id,
                                        reply_to_message_id=ReplyCheck(message),
                                        hide_via=True)