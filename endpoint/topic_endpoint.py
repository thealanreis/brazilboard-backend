from endpoint.generic_endpoint import GenericEndpoint
from model.post import Post
from model.topic import Topic

get_one = {
    'route': '/forum/<forum_uuid>/topic/<topic_uuid>', 'fields': (
        'uuid', 'name', 'created', 'owner.username', 'owner.uuid', 'posts'), 'perm': 'read_topic', 'payload_field': 'topic_uuid'
}

get_all = {
    'route': '/forum/<forum_uuid>/topic',
    'fields': ('name', 'uuid', 'created', 'topics'), 'perm': 'read_topic'
}

update = {
    'route': '/forum/<forum_uuid>/topic/<topic_uuid>/',
    'payload_field': 'topic_uuid', 'update_fields': {'name': 'name', 'first_post_content': 'first_post_content'}
}

create = {
    'route': '/forum/<forum_uuid>/topic/',
    'payload_field': 'topic_uuid', 'create_fields': {'owner_id': 'SESSION_id', 'name': 'name', 'forum_uuid': 'forum_uuid'}, 'children': [Post],
    'children_params': {'post': {'owner_id': 'SESSION_id', 'content': 'first_post_content', 'topic_uuid': 'PARENT_uuid'}}
}

delete = {
    'route': '/forum/<forum_uuid>/topic/',
    'perm': 'delete_post', 'payload_field': 'topic_uuid',
    'check_owner': {'owner_id': 'id'}
}


topic_endpoint = GenericEndpoint(
    Topic, id_field='uuid',  get_one=get_one, get_all=get_all, update=update, create=create, delete=delete)

# @topic_endpoint.route('/forum/<forum_uuid>/topic/<topic_uuid>', 'read_topic')
# def get_topic(get):
#     topic_ = Topic.query.filter_by(uuid=get['topic_uuid']).first()
#     fields = ('uuid', 'name', 'created', 'owner.username', 'owner.uuid', 'posts')
#     return topic_.to_dict(only=fields)

# @topic_endpoint.route('/forum/<forum_uuid>/topic', 'read_topic')
# def get_topics(get):
#     forum_uuid = get['forum_uuid']
#     forum_ = Forum.query.filter_by(uuid=forum_uuid).first()
#     fields = ('name', 'uuid', 'created', 'topics')
#     return forum_.to_dict(fields)


# @topic_endpoint.route('/forum/<forum_uuid>/topic/create', 'write_topic')
# def create_topic(post):
#     forum_uuid = post['forum_uuid']

#     post_: Post = Post()
#     topic: Topic = Topic()
#     owner_ = get_logged_user()

#     topic.forum_uuid = forum_uuid
#     topic.owner_id = owner_.id
#     topic.name = post['name']
#     db.session.add(topic)
#     db.session.flush()

#     post_.content = post['content']
#     post_.owner_id = owner_.id
#     post_.topic_uuid = topic.uuid
#     db.session.add(post_)

#     db.session.commit()


# @topic_endpoint.route('/forum/<forum_uuid>/topic/<topic_uuid>/update', 'edit_topic')
# def update_topic(post):
#     topic_uuid = post['topic_uuid']
#     topic_ = Topic.query.filter_by(uuid=topic_uuid).first()

#     topic_.name = post['name']
#     topic_.posts[0].content = post['content']
#     db.session.add(topic_)
#     commit(topic_)
