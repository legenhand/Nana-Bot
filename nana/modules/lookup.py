from asyncio import sleep
from datetime import datetime

from pyrogram import filters
from pyrogram.errors import PeerIdInvalid

from nana import app, Command, AdminSettings, edrep
from nana.helpers.aiohttp_helper import AioHttp


@app.on_message(filters.user(AdminSettings) & filters.command("lookup", Command))
async def lookup(client, message):
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
        user = await client.get_chat(get_user)
    except PeerIdInvalid:
        await edrep(message, text="I don't know that User.")
        sleep(2)
        await message.delete()
        return
    url = f'https://api.intellivoid.net/spamprotection/v1/lookup?query={user.id}'
    a = await AioHttp().get_json(url)
    response = a['success']
    if response == True:
        date = a["results"]["last_updated"]
        stats = f'**◢ Intellivoid• SpamProtection Info**:\n'
        stats += f' - **Updated on**: `{datetime.fromtimestamp(date).strftime("%Y-%m-%d %I:%M:%S %p")}`\n'
        stats += f' - **Chat Info**: [Link](t.me/SpamProtectionBot/?start=00_{user.id})\n'
        
        if a["results"]["attributes"]["is_potential_spammer"] == True:
            stats += f' - **User**: `USERxSPAM`\n'
        elif a["results"]["attributes"]["is_operator"] == True:
            stats += f' - **User**: `USERxOPERATOR`\n'
        elif a["results"]["attributes"]["is_agent"] == True:
            stats += f' - **User**: `USERxAGENT`\n'
        elif a["results"]["attributes"]["is_whitelisted"] == True:
            stats += f' - **User**: `USERxWHITELISTED`\n'
    
        stats += f' - **Type**: `{a["results"]["entity_type"]}`\n'
        stats += f' - **Language**: `{a["results"]["language_prediction"]["language"]}`\n'
        stats += f' - **Language Probability**: `{a["results"]["language_prediction"]["probability"]}`\n'
        stats += f'**Spam Prediction**:\n'
        stats += f' - **Ham Prediction**: `{a["results"]["spam_prediction"]["ham_prediction"]}`\n'
        stats += f' - **Spam Prediction**: `{a["results"]["spam_prediction"]["spam_prediction"]}`\n'
        stats += f'**Blacklisted**: `{a["results"]["attributes"]["is_blacklisted"]}`\n'
        if a["results"]["attributes"]["is_blacklisted"] == True:
            stats += f' - **Reason**: `{a["results"]["attributes"]["blacklist_reason"]}`\n'
            stats += f' - **Flag**: `{a["results"]["attributes"]["blacklist_flag"]}`\n'
        stats += f'**TELEGRAM HASH**:\n`{a["results"]["private_telegram_id"]}`\n'
        await edrep(message, text=stats, disable_web_page_preview=True)
    else:
        await edrep(message, text='`cannot reach SpamProtection API`')
        await sleep(3)
        await message.delete()