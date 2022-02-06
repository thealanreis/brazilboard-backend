from common.custom_exception import CustomException
from common.jsonify import jsonify_list
from datatabase.dao.dao_generic import commit, delete
from datatabase.dao.dao_user import get_logged_user
from datatabase.model.post import Post
from datatabase.model.topic import Topic
from flask import session, g


def get_posts(json):
    topic_uuid = json['topic_uuid']
    fields = ('uuid', 'name', 'created',
              'owner.username', 'owner.uuid', 'posts')
    _topic = Topic.query.filter_by(uuid=topic_uuid).first()
    return _topic.to_dict(only=fields)


def create_post(json):
    post = Post()
    owner = get_logged_user()
    post.topic_uuid = json['topic_uuid']
    post.content = json['content']
    post.owner_id = owner.id
    commit(post)
    return post.to_dict()


def update_post(json):
    owner_id = session.get('id')
    uuid = json['uuid']
    content = json['content']

    if 'edit_any_post' in g.acl:
        post_ = Post.query.filter_by(uuid=uuid).first()

    elif 'edit_post' in g.acl:
        post_ = Post.query.filter_by(uuid=uuid, owner_id=owner_id).first()

    if post_:
        post_.content = content
        commit(post_)
        return post_.to_dict()

    else:
        raise CustomException('Você não pode editar este post')


def delete_post(json):
    owner_id = session.get('id')
    uuid = json['uuid']

    if 'delete_any_post' in g.acl:
        post_ = Post.query.filter_by(uuid=uuid).first()

    elif 'delete_post' in g.acl:
        post_ = Post.query.filter_by(uuid=uuid, owner_id=owner_id).first()

    if post_:
        post_obj = post_.to_dict()
        delete(post_)
        return post_obj

    else:
        raise CustomException('Você não pode deletar este post')
