from endpoint.generic_endpoint import GenericEndpoint
from common.dao_generic import commit
from endpoint.user_endpoint import get_logged_user
from model.forum import Forum
from model.post import Post
from model.topic import Topic
from backend import db

topic_endpoint = GenericEndpoint()

@topic_endpoint.route('/forum/<fuuid>/topic/<tuuid>', 'read_topic')
def get_topic(get):
    topic_ = Topic.query.filter_by(uuid=get['tuuid']).first()
    fields = ('uuid', 'name', 'created', 'owner.username', 'owner.uuid', 'posts')
    return topic_.to_dict(only=fields)

@topic_endpoint.route('/forum/<fuuid>/topic', 'read_topic')
def get_topics(get):
    forum_uuid = get['fuuid']
    forum_ = Forum.query.filter_by(uuid=forum_uuid).first()
    fields = ('name', 'uuid', 'created', 'topics')
    return forum_.to_dict(fields)

@topic_endpoint.route('/forum/<fuuid>/topic/create', 'write_topic')
def create_topic(post):
    forum_uuid = post['fuuid']

    post_: Post = Post()
    topic: Topic = Topic()
    owner_ = get_logged_user()

    topic.forum_uuid = forum_uuid
    topic.owner_id = owner_.id
    topic.name = post['name']
    db.session.add(topic)
    db.session.flush()

    post_.content = post['content']
    post_.owner_id = owner_.id
    post_.topic_uuid = topic.uuid
    db.session.add(post_)

    db.session.commit()
    
@topic_endpoint.route('/forum/<fuuid>/topic/<tuuid>/update', 'edit_topic')
def update_topic(post):
    topic_uuid = post['tuuid']
    topic_ = Topic.query.filter_by(uuid=topic_uuid).first()

    topic_.name = post['name']
    topic_.posts[0].content = post['content']
    db.session.add(topic_)
    commit(topic_)

    