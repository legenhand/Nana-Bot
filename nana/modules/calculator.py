import os
import sys
import traceback

from currency_converter import CurrencyConverter
from pyrogram import Filters

from nana import app, Command, logging

__MODULE__ = "Calculator"
__HELP__ = """
Calculator, converting, math, etc.

──「 **Evaluation** 」──
-> `eval (math)`
Example: `eval 1+1`
Math can be used: `+, -, *, /`

──「 **Money converter** 」──
-> `curr (value) (from) (to)`
Examlpe: `curr 100 USD IDR`
Output: `USD 100 = IDR 1,409,500.40`

──「 **Temperature converter** 」──
-> `temp (value) (Type)`
Examlpe: `temp 30 C`
Output: `30°C = 86.0°F`
"""

c = CurrencyConverter()


# For converting
def convert_f(fahrenheit):
    f = float(fahrenheit)
    f = (f * 9 / 5) + 32
    return f


def convert_c(celsius):
    cel = float(celsius)
    cel = (cel - 32) * 5 / 9
    return cel


@app.on_message(Filters.me & Filters.command(["eval"], Command))
async def evaluation(client, message):
    if len(message.text.split()) == 1:
        await message.edit("Usage: `eval 1000-7`")
        return
    q = message.text.split(None, 1)[1]
    try:
        ev = str(eval(q))
        if ev:
            if len(ev) >= 4096:
                file = open("nana/cache/output.txt", "w+")
                file.write(ev)
                file.close()
                await client.send_file(message.chat.id, "nana/cache/output.txt",
                                       caption="`Output too large, sending as file`")
                os.remove("nana/cache/output.txt")
                return
            else:
                await message.edit("**Query:**\n{}\n\n**Result:**\n`{}`".format(q, ev))
                return
        else:
            await message.edit("**Query:**\n{}\n\n**Result:**\n`None`".format(q))
            return
    except:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        errors = traceback.format_exception(etype=exc_type, value=exc_obj, tb=exc_tb)
        await message.edit("Error: `{}`".format(errors))
        logging.exception("Evaluation error")


@app.on_message(Filters.me & Filters.command(["curr"], Command))
async def evaluation_curr(_client, message):
    if len(message.text.split()) <= 3:
        await message.edit("Usage: `curr 100 USD IDR`")
        return
    value = message.text.split(None, 3)[1]
    curr1 = message.text.split(None, 3)[2].upper()
    curr2 = message.text.split(None, 3)[3].upper()
    try:
        conv = c.convert(int(value), curr1, curr2)
        text = "{} {} = {} {}".format(curr1, value, curr2, f'{conv:,.2f}')
        await message.edit(text)
    except ValueError as err:
        await message.edit(str(err))


@app.on_message(Filters.me & Filters.command(["temp"], Command))
async def evaluation_temp(_client, message):
    if len(message.text.split()) <= 2:
        await message.edit("Usage: `temp 30 C` or `temp 60 F`")
        return
    temp1 = message.text.split(None, 2)[1]
    temp2 = message.text.split(None, 2)[2]
    try:
        if temp2 == "F":
            result = convert_c(temp1)
            text = "`{}°F` = `{}°C`".format(temp1, result)
            await message.edit(text)
        elif temp2 == "C":
            result = convert_f(temp1)
            text = "`{}°C` = `{}°F`".format(temp1, result)
            await message.edit(text)
        else:
            await message.edit("Unknown type {}".format(temp2))
    except ValueError as err:
        await message.edit(str(err))
