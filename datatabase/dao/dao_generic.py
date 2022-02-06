from backend import db


def commit(obj: object):
    db.session.add(obj)
    db.session.commit()


def delete(obj: object):
    db.session.delete(obj)
    db.session.commit()
