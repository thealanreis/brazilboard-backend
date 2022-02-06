from sqlalchemy_serializer import SerializerMixin
from backend import db
from datetime import datetime as dt
from common.password_utils import generate_password_hash
from common.uuid_utils import generate_uuid
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model, SerializerMixin):

    serialize_only = ('uuid', 'username','picture_uploaded', 'created', 'active')

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(), default=generate_uuid)
    username = db.Column(db.String())
    email = db.Column(db.String())
    _password = db.Column('password', db.String())
    role_id = db.Column(db.Integer, db.ForeignKey(
        "role.id"), nullable=False)
    picture_uploaded = db.Column(db.Boolean(), default=False)
    created = db.Column(db.TIMESTAMP, default=dt.now())
    last_login = db.Column(db.TIMESTAMP, default=dt.now())
    active = db.Column(db.Boolean(), default=True)
    role = db.relationship('Role', backref=db.backref('users'))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)
