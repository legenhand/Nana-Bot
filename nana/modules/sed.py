import re
import sre_constants

from pyrogram import Filters

from nana import app

__MODULE__ = "Sed"
__HELP__ = """
Need help?
Learn regex here: regexone.com

──「 **Regex** 」──
-> `s/(regex)`
Yes, just reply a msg and do `s/test/text`.

Example: "This is test"
Reply: s/test/text
Result: "This is text"

Flags: i (ignore), g (global)
Flag text: `test things test`
Flag ex: s/test/text/g
Flag result: `text things text`
"""

DELIMITERS = ("/", ":", "|", "_")


async def separate_sed(sed_string):
    if (
            len(sed_string) >= 3
            and sed_string[3] in DELIMITERS
            and sed_string.count(sed_string[3]) >= 2
    ):
        delim = sed_string[3]
        start = counter = 4
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None

        while counter < len(sed_string):
            if (
                    sed_string[counter] == "\\"
                    and counter + 1 < len(sed_string)
                    and sed_string[counter + 1] == delim
            ):
                sed_string = sed_string[:counter] + sed_string[counter + 1:]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()


@app.on_message(Filters.me & Filters.regex("^s/(.*?)"))
async def sed_msg(client, message):
    sed_result = await separate_sed("s/" + message.text)
    if sed_result:
        if message.reply_to_message:
            to_fix = message.reply_to_message.text
            if to_fix is None:
                to_fix = message.reply_to_message.caption
                if to_fix is None:
                    return
        else:
            return
        repl, repl_with, flags = sed_result
        if not repl:
            return

        try:
            check = re.match(repl, to_fix, flags=re.IGNORECASE)
            if check and check.group(0).lower() == to_fix.lower():
                return

            if "i" in flags and "g" in flags:
                text = re.sub(repl, repl_with, to_fix, flags=re.I).strip()
            elif "i" in flags:
                text = re.sub(repl, repl_with, to_fix, count=1, flags=re.I).strip()
            elif "g" in flags:
                text = re.sub(repl, repl_with, to_fix).strip()
            else:
                text = re.sub(repl, repl_with, to_fix, count=1).strip()
        except sre_constants.error:
            print("SRE constant error")
            await message.edit("SRE constant error. You can learn regex in [here](https://regexone.com)",
                               disable_web_page_preview=True)
            return
        if text:
            await client.edit_message_text(message.chat.id, message_id=message.message_id,
                                           text="Did you you mean:\n```{}```".format(text))
