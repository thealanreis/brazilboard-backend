from sqlalchemy_serializer import SerializerMixin
from backend import db
from datetime import datetime as dt
from common.uuid_utils import generate_uuid

class Role(db.Model, SerializerMixin):
    serialize_only = ( 'id', 'name', 'description')
    __tablename__ = 'role'
    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
