from typing import List
from flask import session

from model.user import User


def string_to_property(o: dict, obj: object, parameters: List):

    for parameter in parameters:
        if parameter in ['user', 'owner']:
            setattr(obj, parameter, get_user())

        elif parameter in ['user_id', 'owner_id']:
            setattr(obj, parameter, session['id'])

        else:
            setattr(obj, parameter, o[parameter])

    return obj


def get_user():
    uuid = session['uuid']
    return User.query.filter_by(uuid=uuid).first()
