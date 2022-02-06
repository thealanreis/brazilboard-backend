from sqlalchemy_serializer import SerializerMixin
from backend import db
from datetime import datetime as dt
from common.uuid_utils import generate_uuid

# class ModeratorACL(db.Model, SerializerMixin):
#     # serialize_only = ('uuid', 'name')
#     __tablename__ = 'moderator_acl'
#     id = db.Column(db.Integer, primary_key=True)
#     forum_uuid = db.Column(db.String(), db.ForeignKey("forum.uuid"), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)    
#     user = db.relationship('User')
#     forum = db.relationship('Forum', backref=db.backref('moderators'))
    
#     def __init__(self, forum_uuid, user_id):
#         self.forum_uuid = forum_uuid
#         self.user_id = user_id