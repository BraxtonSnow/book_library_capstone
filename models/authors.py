import uuid 
from sqlalchemy.dialects.postgresql import UUID 
import marshmallow as ma

from db import db 
from .authors_books_xref import authors_books_association_table



class Authors(db.Model):
    __tablename__= "Authors"

    author_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author_name = db.Column(db.String(), nullable=False)
    date_of_birth = db.Column(db.String())
    background = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)

    books = db.relationship("Books", secondary=authors_books_association_table, back_populates="authors")

    def __init__(self, author_name, date_of_birth, background, active):
        self.author_name = author_name
        self.date_of_birth = date_of_birth
        self.background = background
        self.active = active


    def get_new_author():
        return Authors("", "", "", True)
    

class AuthorsSchema(ma.Schema):
    class Meta:
        fields = ["author_id", "author_name", "date_of_birth", "background", "books", "active"]

    books = ma.fields.Nested("BooksSchema", many=True, exclude=["authors"])


author_schema = AuthorsSchema()
authors_schema = AuthorsSchema(many=True)