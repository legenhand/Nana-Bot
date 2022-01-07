import re
from html import escape

from pyrogram import filters

from nana import app, Command, AdminSettings, edrep

__MODULE__ = "Stylish Text"
__HELP__ = """
Convert your text to stylish text!

Use this custom format: [Click here to Read](https://telegra.ph/Nana-Remix-Stylish-Text-Helper-07-17)

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
graffiti = u" 𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
graffitib = u" 𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
handwriting = u" 𝒜𝐵𝒞𝒟𝐸𝐹𝒢𝐻𝐼𝒥𝒦𝐿𝑀𝒩𝒪𝒫𝒬𝑅𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝒶𝒷𝒸𝒹𝑒𝒻𝑔𝒽𝒾𝒿𝓀𝓁𝓂𝓃𝑜𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
handwritingb = u" 𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃\"'#$%&()*+,-./:;<=>?@[\\]^_`{|}~"

CHAR_OVER = chr(0x0305)
CHAR_UNDER = chr(0x0332)
CHAR_STRIKE = chr(0x0336)
CHAR_POINTS = chr(0x0324)


def text_style_generator(text, text_type):
    teks = list(text)
    for i, _ in enumerate(teks):
        teks[i] = text_type + teks[i]
    pesan = ""
    for tek in teks:
        pesan += tek
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
        unic = {ord(x[0]): x[1] for x in zip(normaltext, smallcaps)}
        convtext = x.translate(unic)
        text = re.sub(r'<smallcaps>(.*?)</smallcaps>', convtext, text, 1)

    # Converting to superscript text: superscript
    superscript_compile = re.compile(r'<superscript>(.*?)</superscript>')
    src_code = superscript_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, superscript)}
        convtext = x.translate(unic)
        text = re.sub(r'<superscript>(.*?)</superscript>', convtext, text, 1)

    # Converting to subscript text: subscript
    subscript_compile = re.compile(r'<subscript>(.*?)</subscript>')
    src_code = subscript_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, subscript)}
        convtext = x.translate(unic)
        text = re.sub(r'<subscript>(.*?)</subscript>', convtext, text, 1)

    # Converting to wide text: wide
    wide_compile = re.compile(r'<wide>(.*?)</wide>')
    src_code = wide_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, wide)}
        convtext = x.translate(unic)
        text = re.sub(r'<wide>(.*?)</wide>', convtext, text, 1)

    # Converting to bubble text: bubble
    bubble_compile = re.compile(r'<bubble>(.*?)</bubble>')
    src_code = bubble_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, bubbles)}
        convtext = x.translate(unic)
        text = re.sub(r'<bubble>(.*?)</bubble>', convtext, text, 1)

    # Converting to bubblesblack text: bubble2
    bubble2_compile = re.compile(r'<bubble2>(.*?)</bubble2>')
    src_code = bubble2_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, bubblesblack)}
        convtext = x.translate(unic)
        text = re.sub(r'<bubble2>(.*?)</bubble2>', convtext, text, 1)

    # Converting to smothtext text: smothtext
    smoth_compile = re.compile(r'<smoth>(.*?)</smoth>')
    src_code = smoth_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, smothtext)}
        convtext = x.translate(unic)
        text = re.sub(r'<smoth>(.*?)</smoth>', convtext, text, 1)
    graffiti_compile = re.compile(r'<graffiti>(.*?)</graffiti>')
    src_code = graffiti_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, graffiti)}
        convtext = x.translate(unic)
        text = re.sub(r'<graffiti>(.*?)</graffiti>', convtext, text, 1)
    handwriting_compile = re.compile(r'<handwriting>(.*?)</handwriting>')
    src_code = handwriting_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, handwriting)}
        convtext = x.translate(unic)
        text = re.sub(r'<handwriting>(.*?)</handwriting>', convtext, text, 1)

    handwritingb_compile = re.compile(r'<handwritingb>(.*?)</handwritingb>')
    src_code = handwritingb_compile.findall(text)
    for x in src_code:
        unic = {ord(x[0]): x[1] for x in zip(normaltext, handwritingb)}
        convtext = x.translate(unic)
        text = re.sub(r'<handwritingb>(.*?)</handwritingb>', convtext, text, 1)
    return text


@app.on_message(filters.user(AdminSettings) & filters.command("stylish", Command))
async def stylish_generator(_client, message):
    if message.text and len(message.text.split()) == 1 or message.caption and len(message.caption.split()) == 1:
        await edrep(message, text="Usage: `stylish your text goes here`")
        return

    if message.caption:
        text = message.caption.split(None, 1)[1]
    else:
        text = message.text.split(None, 1)[1]

    text = stylish_formatting(text)

    if message.caption:
        await message.edit_caption(text)
    else:
        await edrep(message, text=text)


# For inline stuff
def formatting_text_inline(text, text_style):
    unic = {ord(x[0]): x[1] for x in zip(normaltext, text_style)}
    return text.translate(unic)


def upsidedown_text_inline(text):
    line = text.strip("\r\n")
    text = ''.join(upsidedown_dict[c] if c in upsidedown_dict else c for c in line[::-1])
    return text
