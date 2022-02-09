from sqlalchemy_serializer import SerializerMixin
from backend import db

class ForumACL(db.Model, SerializerMixin):
    # serialize_only = ('forum_uuid', 'role_id', 'read', 'write')
    __tablename__ = 'forum_acl'
    
    id = db.Column(db.Integer, primary_key=True)
    forum_uuid = db.Column(db.String(), db.ForeignKey("forum.uuid"), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    read_topic = db.Column(db.Boolean, default=False)
    write_topic = db.Column(db.Boolean, default=False)
    edit_topic = db.Column(db.Boolean, default=False)
    delete_topic = db.Column(db.Boolean, default=False)
    write_post = db.Column(db.Boolean, default=False)
    edit_post = db.Column(db.Boolean, default=False)
    delete_post = db.Column(db.Boolean, default=False)
    write_pool = db.Column(db.Boolean, default=False)
    edit_pool = db.Column(db.Boolean, default=False)
    delete_pool = db.Column(db.Boolean, default=False)
    
    role = db.relationship('Role')
    forum = db.relationship('Forum', backref=db.backref('acls'))

    # def __init__(self, forum_uuid, role_id, read_topic, write_topic, edit_topic, delete_topic, write_post, edit_post, delete_post):
    #     self.forum_uuid = forum_uuid
    #     self.role_id = role_id
    #     self.read_topic = read_topic
    #     self.write_topic = write_topic
    #     self.edit_topic = edit_topic
    #     self.delete_topic = delete_topic
    #     self.write_post = write_post
    #     self.edit_post = edit_post
    #     self.delete_post = delete_post