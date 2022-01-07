from sqlalchemy import Column, String, UnicodeText

from nana import BASE, SESSION


class MyChats(BASE):
    __tablename__ = "my_chats"
    chat_id = Column(String(14), primary_key=True)
    chat_name = Column(UnicodeText, nullable=False)
    chat_username = Column(UnicodeText)

    def __init__(self, chat_id, chat_name, chat_username):
        "initializing db"
        self.chat_id = str(chat_id)
        self.chat_name = chat_name
        self.chat_username = chat_username

    def __repr__(self):
        "chat message for db"
        return "<Chat {} ({})>".format(self.chat_name, self.chat_id)


MyChats.__table__.create(checkfirst=True)

MY_ALL_CHATS = {}


def update_chat(chat):
    global MY_ALL_CHATS
    if (
        chat.id in list(MY_ALL_CHATS)
        and MY_ALL_CHATS.get(chat.id)
        and MY_ALL_CHATS[chat.id].get('name') == chat.title
        and MY_ALL_CHATS[chat.id].get('username') == chat.username
    ):
        return
    chat_db = SESSION.query(MyChats).get(str(chat.id))
    if chat_db:
        SESSION.delete(chat_db)
    chat_db = MyChats(str(chat.id), chat.title, chat.username)
    SESSION.add(chat_db)
    SESSION.commit()
    MY_ALL_CHATS[chat.id] = {"name": chat.title, "username": chat.username}


def get_all_chats():
    try:
        return SESSION.query(MyChats).all()
    finally:
        SESSION.close()


def __load_mychats():
    global MY_ALL_CHATS
    try:
        MY_ALL_CHATS = {}
        qall = SESSION.query(MyChats).all()
        for x in qall:
            MY_ALL_CHATS[x.chat_id] = {"name": x.chat_name, "username": x.chat_username}
    finally:
        SESSION.close()


__load_mychats()
