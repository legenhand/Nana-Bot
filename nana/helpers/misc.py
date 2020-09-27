
from pyrogram.types import InlineKeyboardButton


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(_page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [EqInlineKeyboardButton(x.__MODULE__,
                                    callback_data="{}_module({})".format(prefix, x.__MODULE__.lower())) for x
             in module_dict.values()])
    else:
        modules = sorted(
            [EqInlineKeyboardButton(x.__MODULE__,
                                    callback_data="{}_module({},{})".format(prefix, chat, x.__MODULE__.lower())) for x
             in module_dict.values()])

    pairs = [
    modules[i * 3:(i + 1) * 3] for i in range((len(modules) + 3 - 1) // 3)
    ]
    round_num = len(modules) / 3
    calc = len(modules) - round(round_num)
    if calc == 1:
        pairs.append((modules[-1], ))
    elif calc == 2:
        pairs.append((modules[-1],))

    return pairs
