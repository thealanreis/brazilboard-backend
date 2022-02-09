from sqlalchemy_serializer import SerializerMixin
from backend import db
from common.uuid_utils import generate_uuid
from model.post import Post
from datetime import datetime as dt
class Topic(db.Model, SerializerMixin):

    serialize_only = ('uuid', 'name', 'created', 'owner.username', 'owner.uuid')
    __tablename__ = 'topic'

    uuid = db.Column(db.String(), default=generate_uuid, primary_key=True)
    name = db.Column(db.String())
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "user.id"), nullable=False)
    forum_uuid = db.Column(db.Integer, db.ForeignKey(
        "forum.uuid"), nullable=False)        
    created = db.Column(db.TIMESTAMP, default=dt.now)
    owner = db.relationship('User', backref=db.backref('topics'))
    posts = db.relationship('Post', backref=db.backref('topic'), order_by="asc(Post.created)")