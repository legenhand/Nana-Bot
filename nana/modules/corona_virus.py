
import asyncio
from pyrogram import Filters

from nana import Command, app
from nana.helpers.aiohttp_helper import AioHttp

__MODULE__ = "Covid Info"
__HELP__ = """
Check info of cases corona virus disease 2019

──「 **Info Covid** 」──
-> `covid - for Global Stats`
-> `covid (country) - for a Country Stats`
"""


@app.on_message(Filters.me & Filters.command(["covid"], Command))
async def corona(_client, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        try:
            r = await AioHttp().get_json("https://corona.lmao.ninja/v2/all")
            reply_text = f"**Global Cases 🦠:**\nCases: `{r['cases']:,}`\nCases Today: `{r['todayCases']:,}`\nDeaths: `{r['deaths']:,}`\nDeaths Today: `{r['todayDeaths']:,}`\nRecovered: `{r['recovered']:,}`\nActive: `{r['active']:,}`\nCritical: `{r['critical']:,}`\nCases/Mil: `{r['casesPerOneMillion']}`\nDeaths/Mil: `{r['deathsPerOneMillion']}``"
            await message.edit(f"{reply_text}")
        except Exception as e:
            await message.edit("`The corona API could not be reached`")
            print(e)
            await asyncio.sleep(3)
            await message.delete()
    country = args[1]
    r = await AioHttp().get_json(f"https://corona.lmao.ninja/v2/countries/{country}")
    if "cases" not in r:
        await message.edit("```The country could not be found!```")
        await asyncio.sleep(3)
        await message.delete()
    else:
        try:
            reply_text = f"**Cases for {r['country']} 🦠**\nCases: `{r['cases']:,}`\nCases Today: `{r['todayCases']:,}`\nDeaths: `{r['deaths']:,}`\nDeaths Today: `{r['todayDeaths']:,}`\nRecovered: `{r['recovered']:,}`\nActive: `{r['active']:,}`\nCritical: `{r['critical']:,}`\nCases/Mil: `{r['casesPerOneMillion']}`\nDeaths/Mil: `{r['deathsPerOneMillion']}``"
            await message.edit(f"{reply_text}")
        except Exception as e:
            await message.edit("`The corona API could not be reached`")
            print(e)
            await asyncio.sleep(3)
            await message.delete()