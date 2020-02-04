from math import ceil

from pyrogram import InlineKeyboardButton


class EqInlineKeyboardButton(InlineKeyboardButton):
	def __eq__(self, other):
		return self.text == other.text

	def __lt__(self, other):
		return self.text < other.text

	def __gt__(self, other):
		return self.text > other.text

def paginate_modules(page_n, module_dict, prefix, chat=None):
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

	pairs = list(zip(modules[::2], modules[1::2]))

	if len(modules) % 2 == 1:
		pairs.append((modules[-1],))

	max_num_pages = ceil(len(pairs) / 7)
	modulo_page = page_n % max_num_pages

	# can only have a certain amount of buttons side by side
	if len(pairs) > 7:
		pairs = pairs[modulo_page * 7:7 * (modulo_page + 1)] + [
			(EqInlineKeyboardButton("⬅️", callback_data="{}_prev({})".format(prefix, modulo_page)),
			 EqInlineKeyboardButton("➡️", callback_data="{}_next({})".format(prefix, modulo_page)))]

	return pairs
