from sqlalchemy import Column, UnicodeText, Integer

from nana import BASE, SESSION


class CustomThemeSet(BASE):
    __tablename__ = "custom_theme_set"
    id_theme = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(UnicodeText)
    welcome = Column(UnicodeText)
    start = Column(UnicodeText)
    settings = Column(UnicodeText)
    stats = Column(UnicodeText)

    def __init__(self, name, welcome, start, settings, stats):
        self.name = str(name)
        self.welcome = str(welcome)
        self.start = str(start)
        self.settings = str(settings)
        self.stats = str(stats)

    def __repr__(self):
        return "{}".format(self.name)


CustomThemeSet.__table__.create(checkfirst=True)


async def add_custom_theme(name, welcome, start, settings, stats):
    name_db = CustomThemeSet(name, welcome, start, settings, stats)
    SESSION.add(name_db)
    SESSION.commit()


async def get_list_costum_theme():
    try:
        list_theme = SESSION.query(CustomThemeSet).all()
        list_thm = []
        for i in list_theme:
            list_thm.append([i.name, f"cthm-{i.id_theme}"])
        return list_thm
    finally:
        SESSION.close()


async def get_custom_theme(id_theme):
    a = SESSION.query(CustomThemeSet).filter(CustomThemeSet.id_theme == id_theme).first()
    return {
        "welcome": a.welcome,
        "start": a.start,
        "settings": a.settings,
        "stats": a.stats
    }

