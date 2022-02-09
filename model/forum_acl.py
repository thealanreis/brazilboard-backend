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