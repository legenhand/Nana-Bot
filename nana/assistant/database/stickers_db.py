import threading

from nana import BASE, SESSION
from sqlalchemy import Column, UnicodeText, Integer


class StickerSet(BASE):
	__tablename__ = "sticker_set"
	my_id = Column(Integer, primary_key=True)
	sticker = Column(UnicodeText)

	def __init__(self, my_id, sticker):
		self.my_id = my_id
		self.sticker = str(sticker)

	def __repr__(self):
		return "<Sticker {}>".format(self.my_id)

class StickerAnimationSet(BASE):
	__tablename__ = "sticker_animation_set"
	my_id = Column(Integer, primary_key=True)
	sticker = Column(UnicodeText)

	def __init__(self, my_id, sticker):
		self.my_id = my_id
		self.sticker = str(sticker)

	def __repr__(self):
		return "<Sticker Animation {}>".format(self.my_id)

StickerSet.__table__.create(checkfirst=True)
StickerAnimationSet.__table__.create(checkfirst=True)


def set_sticker_set(my_id, sticker):
	sticker_db = SESSION.query(StickerSet).get(my_id)
	if sticker_db:
		SESSION.delete(sticker_db)
	sticker_db = StickerSet(my_id, sticker)
	SESSION.add(sticker_db)
	SESSION.commit()

def get_sticker_set(my_id):
	try:
		return SESSION.query(StickerSet).get(my_id)
	finally:
		SESSION.close()

def set_stanim_set(my_id, sticker):
	sticker_db = SESSION.query(StickerAnimationSet).get(my_id)
	if sticker_db:
		SESSION.delete(sticker_db)
	sticker_db = StickerAnimationSet(my_id, sticker)
	SESSION.add(sticker_db)
	SESSION.commit()

def get_stanim_set(my_id):
	try:
		return SESSION.query(StickerAnimationSet).get(my_id)
	finally:
		SESSION.close()
