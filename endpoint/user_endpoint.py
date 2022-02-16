from common.file_server import upload_files
from endpoint.generic_endpoint import GenericEndpoint
from common.jsonify import jsonify_list
from common.password_utils import password_match
from common.string_utils import string_to_property
from common.dao_generic import commit
from model.forum_acl import ForumACL
from model.role import Role
from model.user import User
from flask import session

user_endpoint = GenericEndpoint(User)


@user_endpoint.route('/teste/<nome>')
def teste(get):
    return {'msg': get['nome']}


@user_endpoint.route()
def upload_my_avatar(post):
    user_: User = User.query.filter_by(id=session['id']).first()
    user_.picture_uploaded = True
    avatar = post.get('files')
    upload_files(avatar, 'AVATAR', f'{user_.uuid}.png')
    commit(user_)
    return {'ok': 1}


@user_endpoint.route()
def update_my_user(post):
    user_ = User.query.filter_by(id=session['id']).first()
    user_.signature = post['signature']
    commit(user_)


@user_endpoint.route()
def get_my_user(get):
    user_ = User.query.filter_by(id=session['id']).first()
    fields = ('uuid', 'username', 'picture_uploaded',
              'created', 'active', 'signature', 'email')
    return user_.to_dict(only=fields)


@user_endpoint.route()
def get_users(get):
    usernames_ = User.query.all()
    fields = ('id', 'username')
    return jsonify_list(usernames_, fields=fields)


@user_endpoint.route()
def register(post):
    user_ = User()
    role_ = Role.query.filter_by(name='LOGGED_USER').first()
    user_.role_id = role_.id

    user = string_to_property(post, user_, ['username', 'email', 'password'])
    commit(user)


@user_endpoint.route()
def login(post):
    password = post['password']
    user_ = User.query.filter_by(email=post['email']).first()

    # Clear previous session
    if user_ and password_match(password, user_.password):
        clear_session_keys()
        session['uuid'] = user_.uuid
        session['role_id'] = user_.role_id
        session['id'] = user_.id
        session['role_name'] = user_.role.name

        if user_.role.name == 'ADMIN':
            session['is_admin'] = True

        return user_.to_dict()
    else:
        return None


@user_endpoint.route()
def logged_in(get):
    uuid = session.get('uuid')
    if uuid:
        user_ = User.query.filter_by(uuid=uuid).first()
        return user_.to_dict()

    else:
        return None


@user_endpoint.route()
def logout(get):
    clear_session_keys()
    return True


@user_endpoint.route()
def get_roles(get):
    exclude_roles = ['ADMIN', 'MODERATOR']
    roles_ = Role.query.filter(Role.name.not_in(exclude_roles)).all()
    return jsonify_list(roles_)


def get_logged_user():
    uuid = session['uuid']
    return User.query.filter_by(uuid=uuid).first()


def get_user_id():
    return session['id']


def get_acl_entry(forum_uuid, role_id, perm):
    return ForumACL.query.filter(ForumACL.forum_uuid == forum_uuid, ForumACL.role_id == role_id, getattr(ForumACL, perm) == True).first()


def clear_session_keys():
    for key in list(session):
        if not key.startswith('_'):
            session.pop(key)
