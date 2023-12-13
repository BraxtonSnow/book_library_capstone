import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db 
from .genres_books_xref import genres_books_association_table



class Genres(db.Model):
    __tablename__= "Genres"

    genre_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    genre_name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    books = db.relationship("Books", secondary=genres_books_association_table, back_populates="genres")

    def __init__(self, genre_name, description, active):
        self.genre_name = genre_name
        self.description = description
        self.active = active


    def get_new_genre():
        return Genres("", "", True)
    

class GenresSchema(ma.Schema):
    class Meta:
        fields = ["genre_id", "genre_name", "description", "books", "active"]

    books = ma.fields.Nested("BooksSchema", many=True, exclude=["genres"])


genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)