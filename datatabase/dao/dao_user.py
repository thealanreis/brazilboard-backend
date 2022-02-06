from common.jsonify import jsonify_list
from common.password_utils import password_match
from common.string_utils import string_to_property
from datatabase.dao.dao_generic import commit
from datatabase.model.forum_acl import ForumACL
from datatabase.model.role import Role
from datatabase.model.user import User
from flask import session
from backend import db

def get_users(json):
    usernames_ = User.query.all()
    fields = ('id', 'username')
    return jsonify_list(usernames_, fields=fields)
    


def register(json):
    user_ = User()
    role_ = Role.query.filter_by(name='LOGGED_USER').first()
    user_.role_id = role_.id

    user = string_to_property(json, user_, ['username', 'email', 'password'])
    commit(user)


def login(json):
    password = json['password']
    user_ = User.query.filter_by(email=json['email']).first()

    #Clear previous session
    if user_ and password_match(password, user_.password):
        for key in list(session):
            if not key.startswith('_'):
                session.pop(key)
        
        session['uuid'] = user_.uuid
        session['role_id'] = user_.role_id
        session['id'] = user_.id
        session['role_name'] = user_.role.name
        
        if user_.role.name == 'ADMIN':
            session['is_admin'] = True


        return user_.to_dict()
    else:
        return None


def logged_in(json):
    uuid = session.get('uuid')
    if uuid:
        user_ = User.query.filter_by(uuid=uuid).first()
        return user_.to_dict()

    else:
        return None


def get_logged_user():
    uuid = session['uuid']
    return User.query.filter_by(uuid=uuid).first()


def get_user_id():
    return session['id']


def get_roles(json):
    exclude_roles = ['ADMIN','MODERATOR']
    roles_ = Role.query.filter(Role.name.not_in(exclude_roles)).all()
    return jsonify_list(roles_)


def get_acl_entry(forum_uuid, role_id, perm):
    return ForumACL.query.filter(ForumACL.forum_uuid==forum_uuid, ForumACL.role_id==role_id, getattr(ForumACL, perm)==True).first()
