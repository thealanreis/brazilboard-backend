from sqlalchemy_serializer import SerializerMixin
from backend import db

class Role(db.Model, SerializerMixin):
   
    serialize_only = ( 'id', 'name', 'description')
    __tablename__ = 'role'

    id = db.Column(db.Integer,  primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
