from sqlalchemy import Column, UnicodeText, Integer, Boolean

from nana import BASE, SESSION, Owner


class ThemeSet(BASE):
    __tablename__ = "theme_set"
    my_id = Column(Integer, primary_key=True)
    name_theme = Column(UnicodeText)
    is_custom = Column(Boolean)

    def __init__(self, my_id, name_theme):
        self.my_id = my_id
        self.name_theme = str(name_theme)

    def __repr__(self):
        return "{}".format(self.name_theme)


ThemeSet.__table__.create(checkfirst=True)


async def set_name_theme_set(my_id, name_theme, custom):
    name_theme_db = SESSION.query(ThemeSet).get(my_id)
    if name_theme_db:
        SESSION.delete(name_theme_db)
    name_theme_db = ThemeSet(my_id, name_theme, custom)
    SESSION.add(name_theme_db)
    SESSION.commit()


async def get_name_theme_set(my_id):
    try:
        name = SESSION.query(ThemeSet).get(my_id)
        if name:
            return f"{name}"
        else:
            await set_name_theme_set(Owner, "Nana-Official", False)
            return "Nana-Official"

    finally:
        SESSION.close()


async def is_custom_theme():
    is_custom = SESSION.query(ThemeSet).all()
    print(is_custom)