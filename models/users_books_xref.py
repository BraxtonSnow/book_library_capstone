from db import db 

users_books_association_table = db.Table(
    "UserBookAssociation",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("Users.user_id"), primary_key=True),
    db.Column("book_id", db.ForeignKey("Books.book_id"), primary_key=True)
)