import threading

from sqlalchemy import Column, UnicodeText, Numeric

from nana import SESSION, BASE


class Favourites(BASE):
    __tablename__ = "favourites"
    user_id = Column(Numeric, primary_key=True)
    data = Column(UnicodeText, primary_key=True)

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data


Favourites.__table__.create(checkfirst=True)
FAV_INSERTION_LOCK = threading.RLock()


def check_fav(user_id, data):
    try:
        return SESSION.query(Favourites).get((int(user_id), str(data)))
    finally:
        SESSION.close()


def get_fav(user_id):
    try:
        return (
            SESSION.query(Favourites).filter(Favourites.user_id == int(user_id)).all()
        )
    finally:
        SESSION.close()


def add_fav(user_id, data):
    with FAV_INSERTION_LOCK:
        to_check = check_fav(user_id, data)
        if not to_check:
            adder = Favourites(int(user_id), str(data))
            SESSION.add(adder)
            SESSION.commit()
            return True
        return False


def remove_fav(user_id):
    with FAV_INSERTION_LOCK:
        to_check = get_fav(user_id)
        if not to_check:
            return False
        rem = SESSION.query(Favourites).filter(Favourites.user_id == user_id)
        rem.delete()
        SESSION.commit()
        return True


def fav_count():
    try:
        return SESSION.query(Favourites).count()
    finally:
        SESSION.close()