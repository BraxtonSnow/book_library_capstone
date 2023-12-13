import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db 
from .users_books_xref import users_books_association_table
from .authors_books_xref import authors_books_association_table
from .genres_books_xref import genres_books_association_table



class Books(db.Model):
    __tablename__= "Books"

    book_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    authors = db.relationship("Authors", secondary=authors_books_association_table, cascade="all, delete", back_populates="books")
    genres = db.relationship("Genres", secondary=genres_books_association_table, cascade="all, delete", back_populates="books")
    users = db.relationship("Users", secondary=users_books_association_table, back_populates="books")
    images = db.relationship("Images", back_populates='book') 

    def __init__(self, title, description, active):
        self.title = title
        self.description = description
        self.active = active


    def get_new_book():
        return Books("", "", True)
    

class BooksSchema(ma.Schema):
    class Meta:
        fields = ["book_id", "title", "description", "authors", "genres", "users", "images", "active"]

    authors = ma.fields.Nested("AuthorsSchema", many=True, exclude=["books"])
    genres = ma.fields.Nested("GenresSchema", many=True, exclude=["books"])
    users = ma.fields.Nested("UsersSchema", many=True, exclude=["books"])
    images = ma.fields.Nested("ImagesSchema", many=True, exclude=["book"])

book_schema = BooksSchema()
books_schema = BooksSchema(many=True)