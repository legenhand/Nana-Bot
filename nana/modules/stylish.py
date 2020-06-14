import re
from html import escape

from pyrogram import Filters

from nana import app, Command

__MODULE__ = "Stylish Text"
__HELP__ = """
Convert your text to stylish text!

Use this custom format:
-> `<upside>Upside-down text</upside>` = `ʇxəʇ uʍop-əpısp∩`
-> `<oline>Overline text</oline>` = `̅o̅v̅e̅r̅l̅i̅n̅e̅ ̅t̅e̅x̅t̅`
-> `<strike>Strike text</strike>` = `̶s̶t̶r̶i̶k̶e̶ ̶t̶e̶x̶t̶`
-> `<unline>Underline text</unline>` = `̲u̲n̲d̲e̲r̲l̲i̲n̲e̲ ̲t̲e̲x̲t̲`
-> `<point>Point text</point>` = `p̤o̤i̤n̤t̤ ̤t̤e̤x̤t̤`
-> `<smallcaps>Smallcaps text</smallcaps>` = `sᴍᴀʟʟᴄᴀᴘs ᴛᴇxᴛ`
-> `<superscript>Superscript text</superscript>` = `ˢᵘᵖᵉʳˢᶜʳᶦᵖᵗ ᵗᵉˣᵗ`
-> `<subscript>Subscript text</subscript>` = `ₛᵤᵦₛ𝒸ᵣᵢₚₜ ₜₑₓₜ`
-> `<wide>Wide text</wide>` = `ｗｉｄｅ ｔｅｘｔ`
-> `<bubble>Bubbles text</bubble>` = `ⒷⓊⒷⒷⓁⒺⓈ ⓉⒺⓍⓉ`
-> `<bubble2>Bubbles black text</bubble2>` = `🅑🅤🅑🅑🅛🅔🅢 🅑🅛🅐🅒🅚 🅣🅔🅧🅣`
-> `<smoth>Smoth text</smoth>` = `ᔑᗰᝪᎢᕼ Ꭲᗴ᙭Ꭲ`

──「 **Stylish Generator** 」──
-> `stylish Your text here <upside>with</upside> <strike>formatted</strike> <unline>style</unline>`
Stylish your text easily, can be used as caption and text.

Example:
Input = `stylish Your text here <upside>with</upside> <strike>formatted</strike> <unline>style</unline>`
Output = `Your text here ɥʇ!ʍ f̶o̶r̶m̶a̶t̶t̶e̶d̶ s̲t̲y̲l̲e̲`
""".replace("<", escape('<')).replace(">", escape('>'))

upsidedown_dict = {
    'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ə',
    'f': 'ɟ', 'g': 'ɓ', 'h': 'ɥ', 'i': 'ı', 'j': 'ɾ',
    'k': 'ʞ', 'l': 'l', 'm': 'ɯ', 'n': 'u', 'o': 'o',
    'p': 'p', 'q': 'q', 'r': 'ɹ', 's': 's', 't': 'ʇ',
    'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x', 'y': 'ʎ',
    'z': 'z',
    'A': '∀', 'B': 'B', 'C': 'Ↄ', 'D': '◖', 'E': 'Ǝ',
    'F': 'Ⅎ', 'G': '⅁', 'H': 'H', 'I': 'I', 'J': 'ſ',
    'K': 'K', 'L': '⅂', 'M': 'W', 'N': 'ᴎ', 'O': 'O',
    'P': 'Ԁ', 'Q': 'Ό', 'R': 'ᴚ', 'S': 'S', 'T': '⊥',
    'U': '∩', 'V': 'ᴧ', 'W': 'M', 'X': 'X', 'Y': '⅄',
    'Z': 'Z',
    '0': '0', '1': '1', '2': '0', '3': 'Ɛ', '4': 'ᔭ',
    '5': '5', '6': '9', '7': 'Ɫ', '8': '8', '9': '0',
    '_': '¯', "'": ',', ',': "'", '\\': '/', '/': '\\',
    '!': '¡', '?': '¿',
}
normaltext = u" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
smallcaps = u" ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀsᴛᴜᴠᴡxʏᴢ1234567890\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
superscript = u" ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾᵠᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖᵠʳˢᵗᵘᵛʷˣʸᶻ¹²³⁴⁵⁶⁷⁸⁹⁰\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
subscript = u" ₐBCDₑFGₕᵢⱼₖₗₘₙₒₚQᵣₛₜᵤᵥWₓYZₐᵦ𝒸𝒹ₑ𝒻𝓰ₕᵢⱼₖₗₘₙₒₚᵩᵣₛₜᵤᵥ𝓌ₓᵧ𝓏₁₂₃₄₅₆₇₈₉₀\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
wide = u'　ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ０１２３４５６７８９！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［\\］＾＿‘｛｜｝～'
bubbles = u" ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏ1234567890\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
bubblesblack = u" 🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩🅐🅑🅒🅓🅔🅕🅖🅗🅘🅙🅚🅛🅜🅝🅞🅟🅠🅡🅢🅣🅤🅥🅦🅧🅨🅩1234567890\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
smothtext = u" ᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦᏞᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃᗩᗷᑕᗞᗴᖴᏀᕼᏆᒍᏦᏞᗰᑎᝪᑭᑫᖇᔑᎢᑌᐯᗯ᙭ᎩᏃ1234567890\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"

CHAR_OVER = chr(0x0305)
CHAR_UNDER = chr(0x0332)
CHAR_STRIKE = chr(0x0336)
CHAR_POINTS = chr(0x0324)


def text_style_generator(text, text_type):
    teks = list(text)
    for i, _ in enumerate(teks):
        teks[i] = text_type + teks[i]
    pesan = ""
    for x in range(len(teks)):
        pesan += teks[x]
    return pesan + text_type


def stylish_formatting(text):
    # Converting to upside-down text: upside
    upside_compile = re.compile(r'<upside>(.*?)</upside>')
    src_code = upside_compile.findall(text)
    for x in src_code:
        line = x.strip("\r\n")
        xline = ''.join(upsidedown_dict[c] if c in upsidedown_dict else c for c in line[::-1])
        text = re.sub(r'<upside>(.*?)</upside>', xline, text, 1)

    # Converting to overlined: oline
    overlined_compile = re.compile(r'<oline>(.*?)</oline>')
    src_code = overlined_compile.findall(text)
    for x in src_code:
        compiled = text_style_generator(x, CHAR_OVER)
        text = re.sub(r'<oline>(.*?)</oline>', compiled, text, 1)

    # Converting to understrike: unline
    unline_compile = re.compile(r'<unline>(.*?)</unline>')
    src_code = unline_compile.findall(text)
    for x in src_code:
        compiled = text_style_generator(x, CHAR_UNDER)
        text = re.sub(r'<unline>(.*?)</unline>', compiled, text, 1)

    # Converting to strike: strike
    strike_compile = re.compile(r'<strike>(.*?)</strike>')
    src_code = strike_compile.findall(text)
    for x in src_code:
        compiled = text_style_generator(x, CHAR_STRIKE)
        text = re.sub(r'<strike>(.*?)</strike>', compiled, text, 1)

    # Converting to points: point
    point_compile = re.compile(r'<point>(.*?)</point>')
    src_code = point_compile.findall(text)
    for x in src_code:
        compiled = text_style_generator(x, CHAR_POINTS)
        text = re.sub(r'<point>(.*?)</point>', compiled, text, 1)

    # Converting to smallcaps text: smallcaps
    smallcaps_compile = re.compile(r'<smallcaps>(.*?)</smallcaps>')
    src_code = smallcaps_compile.findall(text)
    for x in src_code:
        unic = dict((ord(x[0]), x[1]) for x in zip(normaltext, smallcaps))
        convtext = x.translate(unic)
        text = re.sub(r'<smallcaps>(.*?)</smallcaps>', convtext, text, 1)

    # Converting to superscript text: superscript
    superscript_compile = re.compile(r'<superscript>(.*?)</superscript>')
    src_code = superscript_compile.findall(text)
    for x in src_code:
        unic = dict((ord(x[0]), x[1]) for x in zip(normaltext, superscript))
        convtext = x.translate(unic)
        text = re.sub(r'<superscript>(.*?)</superscript>', convtext, text, 1)

    # Converting to subscript text: subscript
    subscript_compile = re.compile(r'<subscript>(.*?)</subscript>')
    src_code = subscript_compile.findall(text)
    for x in src_code:
        unic = dict((ord(x[0]), x[1]) for x in zip(normaltext, subscript))
        convtext = x.translate(unic)
        text = re.sub(r'<subscript>(.*?)</subscript>', convtext, text, 1)

    # Converting to wide text: wide
    wide_compile = re.compile(r'<wide>(.*?)</wide>')
    src_code = wide_compile.findall(text)
    for x in src_code:
        unic = dict((ord(x[0]), x[1]) for x in zip(normaltext, wide))
        convtext = x.translate(unic)
        text = re.sub(r'<wide>(.*?)</wide>', convtext, text, 1)

    # Converting to bubble text: bubble
    bubble_compile = re.compile(r'<bubble>(.*?)</bubble>')
    src_code = bubble_compile.findall(text)
    for x in src_code:
        unic = dict((ord(x[0]), x[1]) for x in zip(normaltext, bubbles))
        convtext = x.translate(unic)
        text = re.sub(r'<bubble>(.*?)</bubble>', convtext, text, 1)

    # Converting to bubblesblack text: bubble2
    bubble2_compile = re.compile(r'<bubble2>(.*?)</bubble2>')
    src_code = bubble2_compile.findall(text)
    for x in src_code:
        unic = dict((ord(x[0]), x[1]) for x in zip(normaltext, bubblesblack))
        convtext = x.translate(unic)
        text = re.sub(r'<bubble2>(.*?)</bubble2>', convtext, text, 1)

    # Converting to smothtext text: smothtext
    smoth_compile = re.compile(r'<smoth>(.*?)</smoth>')
    src_code = smoth_compile.findall(text)
    for x in src_code:
        unic = dict((ord(x[0]), x[1]) for x in zip(normaltext, smothtext))
        convtext = x.translate(unic)
        text = re.sub(r'<smoth>(.*?)</smoth>', convtext, text, 1)

    return text


@app.on_message(Filters.me & Filters.command(["stylish"], Command))
async def stylish_generator(_client, message):
    if message.text and len(message.text.split()) == 1 or message.caption and len(message.caption.split()) == 1:
        await message.edit("Usage: `stylish your text goes here`")
        return

    if message.caption:
        text = message.caption.split(None, 1)[1]
    else:
        text = message.text.split(None, 1)[1]

    text = stylish_formatting(text)

    if message.caption:
        await message.edit_caption(text)
    else:
        await message.edit(text)


# For inline stuff
def formatting_text_inline(text, text_style):
    unic = dict((ord(x[0]), x[1]) for x in zip(normaltext, text_style))
    conv = text.translate(unic)
    return conv


def upsidedown_text_inline(text):
    line = text.strip("\r\n")
    text = ''.join(upsidedown_dict[c] if c in upsidedown_dict else c for c in line[::-1])
    return text
