"""
Carbon Scraper Plugin for Userbot. //text in creative way.
usage: .carbon //as a reply to any text message

Thanks to @AvinashReddy3108 for a Base Plugin.
Go and Do a star on his repo: https://github.com/AvinashReddy3108/PaperplaneExtended/

"""
import os
from time import sleep
from urllib.parse import quote_plus

from pyrogram import Filters
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from nana import Command, app


@app.on_message(Filters.user("self") & Filters.command(["carbon"], Command))
async def carbon_api(client, message):
    if not message.text[0].isalpha() and message.text[0] not in ("/", "#", "@", "!"):
        """ A Wrapper for carbon.now.sh """
        await message.edit("Processing...")
        CARBON = 'https://carbon.now.sh/?l={lang}&code={code}'
        CARBONLANG = "en"
        textx = message.reply_to_message
        pcode = message.text
        if pcode[8:]:
            pcode = str(pcode[8:])
        elif textx:
            pcode = str(textx.text)  # Importing message to module
        code = quote_plus(pcode)  # Converting to urlencoded
        url = CARBON.format(code=code, lang=CARBONLANG)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = "/usr/bin/google-chrome"
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--disable-gpu')
        prefs = {'download.default_directory': './'}
        chrome_options.add_experimental_option('prefs', prefs)
        await message.edit("Processing 30%")

        driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
        driver.get(url)
        download_path = './'
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_path}}
        command_result = driver.execute("send_command", params)

        driver.find_element_by_xpath("//button[contains(text(),'Export')]").click()
        sleep(5)  # this might take a bit.
        driver.find_element_by_xpath("//button[contains(text(),'4x')]").click()
        sleep(5)
        await message.edit("Processing 50%")
        driver.find_element_by_xpath("//button[contains(text(),'PNG')]").click()
        sleep(5)  # Waiting for downloading

        await message.edit("Processing 90%")
        file = './carbon.png'
        await message.edit("Done!!")
        await client.send_document(
            message.chat.id,
            file,
            caption="Made using [Carbon](https://carbon.now.sh/about/), a project by [Dawn Labs](https://dawnlabs.io/)",
        )

        os.remove('./carbon.png')
        # Removing carbon.png after uploading
        await message.delete()  # Deleting msg
