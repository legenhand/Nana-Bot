import asyncio
import math

import heroku3
import requests
from pyrogram import filters

from nana import app, Command, HEROKU_API, AdminSettings, edrep

# ================= CONSTANT =================
Heroku = heroku3.from_key(HEROKU_API)
heroku_api = "https://api.heroku.com"
# ================= CONSTANT =================


@app.on_message(filters.user(AdminSettings) & filters.command("usage", Command))
async def usage(client, message):
    useragent = ('Mozilla/5.0 (Linux; Android 10; SM-G975F) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/80.0.3987.149 Mobile Safari/537.36')
    u_id = Heroku.account().id
    headers = {
        'User-Agent': useragent,
        'Authorization': f'Bearer {HEROKU_API}',
        'Accept': 'application/vnd.heroku+json; version=3.account-quotas',
    }
    path = "/accounts/" + u_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await edrep(message, text="`Error: something bad happened`\n\n"
                                  f">.`{r.reason}`\n")
    result = r.json()
    quota = result['account_quota']
    quota_used = result['quota_used']

    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)

    App = result['apps']
    try:
        App[0]['quota_used']
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]['quota_used'] / 60
        AppPercentage = math.floor(App[0]['quota_used'] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    message_usage = f"**Total Dyno Usage:** `{AppHours}`**h**  `{AppMinutes}`**m** |  `{AppPercentage}`**%**\n"
    message_usage += f"**Available in month**: `{hours}`**h**  `{minutes}`**m** |  `{percentage}`**%**"
    await asyncio.sleep(1.5)

    await edrep(message, text=message_usage)