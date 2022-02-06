from common.jsonify import jsonify_list
from common.string_utils import string_to_property
from datatabase.dao.dao_user import get_user_id
from datatabase.model.forum_acl import ForumACL
from datatabase.model.forum import Forum
from datatabase.model.user import User
from backend import db

def get_forum(json):
    forum_uuid = json['forum_uuid']
    forum_ = Forum.query.filter_by(uuid=forum_uuid).first()

    fields = ('uuid', 'name', 'moderators.id', 'moderators.username', 'acls')
    return forum_.to_dict(only=fields)

def get_forums(json):
    fields = ('name', 'uuid', 'created', 'owner.username')
    return jsonify_list(Forum.query.all(), fields=fields)


def create_forum(json):
    forum_: Forum = Forum()
    forum_.owner_id = get_user_id()
    forum: Forum = string_to_property(json, forum_, ['name'])
    db.session.add(forum)
    db.session.flush()

    acls = json['acls']
    for acl in acls:
        forum_acl_ = ForumACL()
        forum_acl_.read_topic = acls[acl]['read_topic']
        forum_acl_.write_topic = acls[acl]['write_topic']
        forum_acl_.edit_topic = acls[acl]['edit_topic']
        forum_acl_.delete_topic = acls[acl]['delete_topic']
        forum_acl_.write_post = acls[acl]['write_post']
        forum_acl_.edit_post = acls[acl]['edit_post']
        forum_acl_.delete_post = acls[acl]['delete_post']
        forum_acl_.role_id = acls[acl]['role_id']
        forum_acl_.forum_uuid = forum_.uuid
        # write_pool =  acls[acl]['write_pool'],
        # edit_pool =  acls[acl]['edit_pool'],
        # delete_pool =  acls[acl]['delete_pool'],
        db.session.add(forum_acl_)

    ids = [user['id'] for user in json['moderators']]
    users_ = User.query.filter(User.id.in_(ids)).all()
    forum.moderators = users_
    db.session.commit()


def update_forum(json):
    print('json', json)
    forum_: Forum = Forum.query.filter_by(uuid=json['forum_uuid']).first()
    forum_.name = json['name']
    # forum: Forum = string_to_property(json, forum_, ['name'])
    db.session.add(forum_)
    db.session.flush()

    acls = json['acls']
    for acl in acls:
        forum_acl_ = ForumACL.query.filter_by(id=acls[acl]['id']).first()
        forum_acl_.read_topic = acls[acl]['read_topic']
        forum_acl_.write_topic = acls[acl]['write_topic']
        forum_acl_.edit_topic = acls[acl]['edit_topic']
        forum_acl_.delete_topic = acls[acl]['delete_topic']
        forum_acl_.write_post = acls[acl]['write_post']
        forum_acl_.edit_post = acls[acl]['edit_post']
        forum_acl_.delete_post = acls[acl]['delete_post']
        # write_pool =  acls[acl]['write_pool'],
        # edit_pool =  acls[acl]['edit_pool'],
        # delete_pool =  acls[acl]['delete_pool'],

        db.session.add(forum_acl_)


    ids = [user['id'] for user in json['moderators']]
    users_ = User.query.filter(User.id.in_(ids)).all()
    forum_.moderators = users_


def delete_forum(json):
    pass

def get_forum_acl(json):
    forum_uuid = json['forum_uuid']
    forum_acls_ = ForumACL.query.filter_by(forum_uuid=forum_uuid).all()
    return jsonify_list(forum_acls_)