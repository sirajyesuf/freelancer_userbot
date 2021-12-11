from tinydb import TinyDB, Query
KEYWORD = Query()
db = TinyDB('db.json')


def insert(keyword):
    return db.insert({'keyword': keyword})


def remove(keyword):
    return db.remove(KEYWORD.keyword == keyword.lower())


def all():
    return db.all()
