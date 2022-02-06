from sqlalchemy_serializer import SerializerMixin
from backend import db
from datetime import datetime as dt
from common.uuid_utils import generate_uuid

class Post(db.Model, SerializerMixin):

    serialize_only = ('uuid', 'content', 'created', 'owner')

    __tablename__ = 'post'
    uuid = db.Column(db.String(), default=generate_uuid, primary_key=True)
    content = db.Column(db.String())
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    topic_uuid = db.Column(db.Integer, db.ForeignKey(
        "topic.uuid"), nullable=False)        
    created = db.Column(db.TIMESTAMP, default=dt.now)
    owner = db.relationship('User', backref=db.backref('posts'))

    

