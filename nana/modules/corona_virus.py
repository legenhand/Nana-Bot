import datetime

import asyncio

from prettytable import PrettyTable
import requests
from pyrogram import Filters

from nana import Command, app

__MODULE__ = "Covid Info"
__HELP__ = """
Check info of cases corona virus disease 2019

──「 **Info Covid** 」──
-> `corona - for Global Stats`
-> `corona (country) - for a Country Stats`
"""


@app.on_message(Filters.me & Filters.command(["corona"], Command))
async def corona(_client, message):
    await message.edit("`Processing...`")
    args = message.text.split(None, 1)
    if len(args) == 1:
        r = requests.get("https://corona.lmao.ninja/v2/all?yesterday=true").json()
        last_updated = datetime.datetime.fromtimestamp(r['updated'] / 1000).strftime("%Y-%m-%d %I:%M:%S")

        ac = PrettyTable()
        ac.header = False
        ac.title = "Global Statistics"
        ac.add_row(["Cases", f"{r['cases']:,}"])
        ac.add_row(["Cases Today", f"{r['todayCases']:,}"])
        ac.add_row(["Deaths", f"{r['deaths']:,}"])
        ac.add_row(["Deaths Today", f"{r['todayDeaths']:,}"])
        ac.add_row(["Recovered", f"{r['recovered']:,}"])
        ac.add_row(["Active", f"{r['active']:,}"])
        ac.add_row(["Critical", f"{r['critical']:,}"])
        ac.add_row(["Cases/Million", f"{r['casesPerOneMillion']:,}"])
        ac.add_row(["Deaths/Million", f"{r['deathsPerOneMillion']:,}"])
        ac.add_row(["Tests", f"{r['tests']:,}"])
        ac.add_row(["Tests/Million", f"{r['testsPerOneMillion']:,}"])
        ac.align = "l"

        await message.edit(f"```{str(ac)}```\nLast updated on: {last_updated}")
    country = args[1]
    r = requests.get(f"https://corona.lmao.ninja/v2/countries/{country}").json()
    if "cases" not in r:
        await message.edit("```The country could not be found!```")
        await asyncio.sleep(3)
        await message.delete()
    else:
        last_updated = datetime.datetime.fromtimestamp(r['updated'] / 1000).strftime("%Y-%m-%d %I:%M:%S")

        cc = PrettyTable()
        cc.header = False
        country = r['countryInfo']['iso3'] if len(r['country']) > 12 else r['country']
        cc.title = f"Corona Cases in {country}"
        cc.add_row(["Cases", f"{r['cases']:,}"])
        cc.add_row(["Cases Today", f"{r['todayCases']:,}"])
        cc.add_row(["Deaths", f"{r['deaths']:,}"])
        cc.add_row(["Deaths Today", f"{r['todayDeaths']:,}"])
        cc.add_row(["Recovered", f"{r['recovered']:,}"])
        cc.add_row(["Active", f"{r['active']:,}"])
        cc.add_row(["Critical", f"{r['critical']:,}"])
        cc.add_row(["Cases/Million", f"{r['casesPerOneMillion']:,}"])
        cc.add_row(["Deaths/Million", f"{r['deathsPerOneMillion']:,}"])
        cc.add_row(["Tests", f"{r['tests']:,}"])
        cc.add_row(["Tests/Million", f"{r['testsPerOneMillion']:,}"])
        cc.align = "l"
        await message.edit(f"```{str(cc)}```\nLast updated on: {last_updated}")


def get_country_data(country, world):
    for country_data in world:
        if country_data["country"] == country:
            return country_data
    return

