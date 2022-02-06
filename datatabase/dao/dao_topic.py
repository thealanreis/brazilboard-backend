from common.jsonify import jsonify_list
from datatabase.dao.dao_generic import commit
from datatabase.dao.dao_user import get_logged_user
from datatabase.model.forum import Forum
from datatabase.model.post import Post
from datatabase.model.topic import Topic
from backend import db

def get_topic(json):
    topic_ = Topic.query.filter_by(uuid=json['topic_uuid']).first()
    fields = ('uuid', 'name', 'created', 'owner.username', 'owner.uuid', 'posts')
    return topic_.to_dict(only=fields)


def get_topics(json):
    forum_uuid = json['forum_uuid']
    forum_ = Forum.query.filter_by(uuid=forum_uuid).first()
    fields = ('name', 'uuid', 'created', 'topics')
    return forum_.to_dict(fields)


def create_topic(json):
    forum_uuid = json['forum_uuid']

    post: Post = Post()
    topic: Topic = Topic()
    owner_ = get_logged_user()

    topic.forum_uuid = forum_uuid
    topic.owner_id = owner_.id
    topic.name = json['name']
    db.session.add(topic)
    db.session.flush()

    post.content = json['content']
    post.owner_id = owner_.id
    post.topic_uuid = topic.uuid
    db.session.add(post)

    db.session.commit()
    

def update_topic(json):
    print(json)
    topic_uuid = json['topic_uuid']
    topic_ = Topic.query.filter_by(uuid=topic_uuid).first()

    topic_.name = json['name']
    topic_.posts[0].content = json['content']
    db.session.add(topic_)
    commit(topic_)

    