from sqlalchemy import Column, String, UnicodeText

from nana import BASE, SESSION, Owner


class Cloner(BASE):
    __tablename__ = "cloner"
    user_id = Column(String(14), primary_key=True)
    first_name = Column(UnicodeText)
    last_name = Column(UnicodeText)
    bio = Column(UnicodeText)

    def __init__(self, user_id, first_name, last_name, bio):
        "intialize cloner db"
        self.user_id = str(user_id)
        self.first_name = first_name
        self.last_name = last_name
        self.bio = bio

    def __repr__(self):
        "clooner message for db"
        return "<Cloner {}>".format(self.user_id)


Cloner.__table__.create(checkfirst=True)


def backup_indentity(first_name, last_name, bio):
    cloner_db = SESSION.query(Cloner).get(str(Owner))
    if cloner_db:
        SESSION.delete(cloner_db)
    cloner_db = Cloner(Owner, first_name, last_name, bio)
    SESSION.add(cloner_db)
    SESSION.commit()


def restore_identity():
    cloner_db = SESSION.query(Cloner).get(str(Owner))
    return cloner_db.first_name, cloner_db.last_name, cloner_db.bio
