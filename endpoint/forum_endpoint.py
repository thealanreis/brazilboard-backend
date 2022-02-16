from endpoint.generic_endpoint import GenericEndpoint
from common.jsonify import jsonify_list
from model.forum_acl import ForumACL
from model.forum import Forum


get_one = {'fields': ('uuid', 'name', 'moderators.id', 'moderators.username', 'acls',
                      'topics'), 'route': '/manage/forum/<forum_uuid>', 'payload_field': 'forum_uuid'}
get_all = {'fields': ('name', 'uuid', 'created', 'owner.username'),
           'route': '/get-forums', 'payload_field': 'forum_uuid'}
delete = {'fields': ('name', 'uuid', 'created', 'owner.username'),
          'route': '/get-forums', 'payload_field': 'forum_uuid'}

create = {'route': '/manage/forum/', 'create_fields': {'owner_id': 'SESSION_id', 'name': 'name', 'moderator_ids': 'moderators'}, 'children': [ForumACL],
          'children_params': {
    'forumacl': {'MULTI_': 'acls', 'read_topic': 'read_topic', 'write_topic': 'write_topic', 'edit_topic': 'edit_topic', 'delete_topic': 'delete_topic',
                 'write_post': 'write_post', 'edit_post': 'edit_post', 'delete_post': 'delete_post', 'forum_uuid': 'PARENT_uuid', 'role_id': 'role_id'}
}}

update = {'route': '/manage/forum/<forum_uuid>/update', 'update_fields': {'name': 'name', 'moderator_ids': 'moderators'}, 'children': [ForumACL], 'payload_field': 'forum_uuid',
          'children_params': {
    'forumacl': {'MULTI_': 'acls', 'ID_': 'id', 'read_topic': 'read_topic', 'write_topic': 'write_topic', 'edit_topic': 'edit_topic', 'delete_topic': 'delete_topic',
                 'write_post': 'write_post', 'edit_post': 'edit_post', 'delete_post': 'delete_post'}
}}

forum_endpoint = GenericEndpoint(
    Forum, id_field='uuid', get_one=get_one, get_all=get_all, delete=delete, create=create, update=update)


# @forum_endpoint.route('/manage/forum/<forum_uuid>')
# def get_forum(get):
#     forum_uuid = get['forum_uuid']
#     forum_ = Forum.query.filter_by(uuid=forum_uuid).first()

#     fields = ('uuid', 'name', 'moderators.id', 'moderators.username', 'acls')
#     return forum_.to_dict(only=fields)


# @forum_endpoint.route('/get-forums')
# def get_forums(get):
#     fields = ('name', 'uuid', 'created', 'owner.username')
#     return jsonify_list(Forum.query.all(), fields=fields)


# @forum_endpoint.route('/manage/forum/create')
# def create_forum(post):
#     forum_: Forum = Forum()
#     forum_.owner_id = session['id']
#     forum: Forum = string_to_property(post, forum_, ['name'])
#     db.session.add(forum)
#     db.session.flush()

#     acls = post['acls']
#     for acl in acls:
#         forum_acl_ = ForumACL()
#         forum_acl_.read_topic = acls[acl]['read_topic']
#         forum_acl_.write_topic = acls[acl]['write_topic']
#         forum_acl_.edit_topic = acls[acl]['edit_topic']
#         forum_acl_.delete_topic = acls[acl]['delete_topic']
#         forum_acl_.write_post = acls[acl]['write_post']
#         forum_acl_.edit_post = acls[acl]['edit_post']
#         forum_acl_.delete_post = acls[acl]['delete_post']
#         forum_acl_.role_id = acls[acl]['role_id']
#         forum_acl_.forum_uuid = forum_.uuid
#         # write_pool =  acls[acl]['write_pool'],
#         # edit_pool =  acls[acl]['edit_pool'],
#         # delete_pool =  acls[acl]['delete_pool'],
#         db.session.add(forum_acl_)

#     ids = [user['id'] for user in post['moderators']]
#     users_ = User.query.filter(User.id.in_(ids)).all()
#     forum.moderators = users_
#     db.session.commit()


# @forum_endpoint.route('/manage/forum/<forum_uuid>/update')
# def update_forum(post):
#     forum_: Forum = Forum.query.filter_by(uuid=post['forum_uuid']).first()
#     forum_.name = post['name']
#     # forum: Forum = string_to_property(json, forum_, ['name'])
#     db.session.add(forum_)
#     db.session.flush()

#     acls = post['acls']
#     for acl in acls:
#         forum_acl_ = ForumACL.query.filter_by(id=acls[acl]['id']).first()
#         forum_acl_.read_topic = acls[acl]['read_topic']
#         forum_acl_.write_topic = acls[acl]['write_topic']
#         forum_acl_.edit_topic = acls[acl]['edit_topic']
#         forum_acl_.delete_topic = acls[acl]['delete_topic']
#         forum_acl_.write_post = acls[acl]['write_post']
#         forum_acl_.edit_post = acls[acl]['edit_post']
#         forum_acl_.delete_post = acls[acl]['delete_post']
#         # write_pool =  acls[acl]['write_pool'],
#         # edit_pool =  acls[acl]['edit_pool'],
#         # delete_pool =  acls[acl]['delete_pool'],

#         db.session.add(forum_acl_)

#     ids = [user['id'] for user in post['moderators']]
#     users_ = User.query.filter(User.id.in_(ids)).all()
#     forum_.moderators = users_


# @forum_endpoint.route('/manage/forum/<forum_uuid>/delete')
# def delete_forum(post):
#     pass


@forum_endpoint.route('/manage/forum/<forum_uuid>/get_forum_acl')
def get_forum_acl(post):
    forum_uuid = post['forum_uuid']
    forum_acls_ = ForumACL.query.filter_by(forum_uuid=forum_uuid).all()
    return jsonify_list(forum_acls_)
