from common.custom_exception import CustomException
from endpoint.generic_endpoint import GenericEndpoint
from common.dao_generic import commit, delete
from endpoint.user_endpoint import get_logged_user
from model.post import Post
from model.topic import Topic
from flask import session, g

post_endpoint = GenericEndpoint()

@post_endpoint.route('/forum/<fuuid>/topic/<tuuid>/post', 'read_topic')
def get_posts(get):
    topic_uuid = get['tuuid']
    fields = ('uuid', 'name', 'created',
              'owner.username', 'owner.uuid', 'posts')
    _topic = Topic.query.filter_by(uuid=topic_uuid).first()
    return _topic.to_dict(only=fields)

@post_endpoint.route('/forum/<fuuid>/topic/<tuuid>/post/create', 'write_post')
def create_post(post):
    post_ = Post()
    owner = get_logged_user()
    post_.topic_uuid = post['tuuid']
    post_.content = post['content']
    post_.owner_id = owner.id
    commit(post_)
    return post_.to_dict()

@post_endpoint.route('/forum/<fuuid>/topic/<tuuid>/post/<post_uuid>/update','edit_post')
def update_post(post):
    owner_id = session.get('id')
    uuid = post['uuid']
    content = post['content']

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

@post_endpoint.route('/forum/<fuuid>/topic/<tuuid>/post/<post_uuid>/delete', 'delete_post')
def delete_post(post):
    owner_id = session.get('id')
    uuid = post['uuid']

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
