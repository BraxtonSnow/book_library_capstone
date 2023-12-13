from db import db 

authors_books_association_table = db.Table(
    "AuthorBookAssociation",
    db.Model.metadata,
    db.Column("author_id", db.ForeignKey("Authors.author_id"), primary_key=True),
    db.Column("book_id", db.ForeignKey("Books.book_id"), primary_key=True)
)