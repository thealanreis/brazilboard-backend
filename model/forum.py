from ast import List
from sqlalchemy_serializer import SerializerMixin
from backend import db
from common.uuid_utils import generate_uuid
from model.topic import Topic
from datetime import datetime as dt

from model.user import User


moderators_ = db.Table('moderator_acl',
                       db.Column('user_id', db.Integer,
                                 db.ForeignKey('user.id')),
                       db.Column('forum_uuid', db.Integer,
                                 db.ForeignKey('forum.uuid'))
                       )


class Forum(db.Model, SerializerMixin):

    serialize_only = ('uuid', 'name', 'created', 'moderators')
    datetime_format = '%d/%m/%Y %H:%M'

    __tablename__ = 'forum'
    uuid = db.Column(db.String(), default=generate_uuid, primary_key=True)
    name = db.Column(db.String())
    owner_id = db.Column(db.Integer, db.ForeignKey(
        "user.id"), nullable=False)
    created = db.Column(db.TIMESTAMP, default=dt.now())
    owner = db.relationship('User', backref=db.backref('forums'))
    topics = db.relationship('Topic', backref=db.backref(
        'forum'), order_by="asc(Topic.created)")
    moderators: List = db.relationship(
        "User", secondary=moderators_, order_by="asc(User.username)")

    @property
    def moderator_ids(self):
        return self.moderators

    @moderator_ids.setter
    def moderator_ids(self, moderators):
        ids = [user['id'] for user in moderators]
        users_ = User.query.filter(User.id.in_(ids)).all()
        self.moderators = users_
