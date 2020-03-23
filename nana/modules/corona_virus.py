import os
import shutil
from datetime import datetime

import requests
from covid import Covid
from pyrogram import Filters

from nana import Command, app

__MODULE__ = "Covid Info"
__HELP__ = """
Check info of cases corona virus disease 2019

──「 **Info Covid** 」──
-> `corona (country)`
"""


@app.on_message(Filters.user("self") & Filters.command(["corona"], Command))
async def corona(client, message):
    await message.edit("`Processing...`")
    args = message.text.split(None, 1)
    if len(args) == 1:
        url = 'https://covid-19-api-2-i54peomv2.now.sh/api/og'
        response = requests.get(url, stream=True)
        with open('og', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        os.rename("og", "og.png")
        await client.send_photo(message.chat.id, "og.png", caption="<a href=\"https://covid-19-api-2-i54peomv2.now.sh"
                                                                   "/api/og\">Source</a>")
        await message.delete()
        os.remove("og.png")
        return
    covid = Covid()
    data = covid.get_data()
    country = args[1]
    country_data = get_country_data(country.capitalize(), data)
    if country_data:
        output_text = "`Confirmed   : {}\n`".format(country_data["confirmed"])
        output_text += "`Active      : {}`\n".format(country_data["active"])
        output_text += "`Deaths      : {}`\n".format(country_data["deaths"])
        output_text += "`Recovered   : {}`\n".format(country_data["recovered"])
        output_text += "`Last update : {}`\n". \
            format(datetime.utcfromtimestamp(country_data["last_update"] // 1000).strftime('%Y-%m-%d %H:%M:%S'))
        output_text += "`Data provided by `<a href=\"https://j.mp/2xf6oxF\">Johns Hopkins University</a>"
    else:
        output_text = "`No information yet about this country!`"
    await message.edit("**Corona Virus Info in {}**:\n\n{}".format(country.capitalize(), output_text))
    # TODO : send location of country
    # await client.send_location(message.chat.id, float(country_data["latitude"]), float(country_data["longitude"]))


def get_country_data(country, world):
    for country_data in world:
        if country_data["country"] == country:
            return country_data
    return

