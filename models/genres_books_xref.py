from db import db 

genres_books_association_table = db.Table(
    "GenreBookAsociation",
    db.Model.metadata,
    db.Column("genre_id", db.ForeignKey("Genres.genre_id"), primary_key=True),
    db.Column("book_id", db.ForeignKey("Books.book_id"), primary_key=True)
)