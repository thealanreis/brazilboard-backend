from endpoint.generic_endpoint import GenericEndpoint
from model.post import Post

create = {
    'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post',
    'create_fields': {'owner_id' : 'SESSION_id', 'content' : 'content', 'topic_uuid' : 'topic_uuid'},
    'perm': 'write_post'
}

get_all = {
    'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post',
    'fields': ('uuid', 'name', 'created', 'owner.username', 'owner.uuid', 'posts'),
    'perm': 'read_topic'
}

delete = {
    'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post',
    'perm': 'delete_post', 'payload_field': 'post_uuid',
    'check_owner': {'owner_id': 'id'}
}

update = {
    'route': '/forum/<forum_uuid>/topic/<topic_uuid>/post',
    'perm': 'edit_post', 'payload_field': 'post_uuid', 'update_fields': {'content' : 'content'},
    'check_owner': {'owner_id': 'id'}
}


post_endpoint = GenericEndpoint(
    Post, create=create, get_all=get_all, delete=delete, id_field='uuid', update=update)


# @post_endpoint.route('/forum/<forum_uuid>/topic/<topic_uuid>/post/<post_uuid>/update', 'edit_post')
# def update_post(post):
#     owner_id = session.get('id')
#     uuid = post['uuid']
#     content = post['content']

#     post_ = Post.query.filter_by(uuid=uuid, owner_id=owner_id).first()

#     if post_:
#         post_.content = content
#         commit(post_)
#         return post_.to_dict()
