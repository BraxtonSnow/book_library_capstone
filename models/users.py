import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db 
from .users_books_xref import users_books_association_table



class Users(db.Model):
    __tablename__= "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    books = db.relationship("Books", secondary=users_books_association_table, back_populates="users")

    def __init__(self, user_name, email, password, active):
        self.user_name = user_name
        self.email = email
        self.password = password
        self.active = active


    def get_new_user():
        return Users("", "", "", True)
    

class UsersSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "user_name", "email", "books", "active"]

    books = ma.fields.Nested("BooksSchema", many=True, exclude=["users"])


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)