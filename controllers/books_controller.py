from flask import jsonify, Response

from db import db 
from util.reflection import populate_object
from lib.authenticate import authenticate
from models.books import Books, books_schema, book_schema
from models.authors import Authors
from models.genres import Genres 
from models.images import Images



# @authenticate
def book_add(req) -> Response:
    post_data = req.form if req.form else req.json
    title = post_data.get("title")
    genre_id = post_data.get("genre_id")
    image_name = post_data.get("image_name")
    author_id = post_data.get("author_id")

    new_record = Books.get_new_book()

    populate_object(new_record, post_data)


    db.session.add(new_record)
    db.session.commit()

    book_query = db.session.query(Books).filter(Books.title == title).first()
    genre_query = db.session.query(Genres).filter(Genres.genre_id == genre_id).first()
    image_query = db.session.query(Images).filter(Images.image_name == image_name).first()
    author_query = db.session.query(Authors).filter(Authors.author_id == author_id).first()

    book_query.authors.append(author_query)
    book_query.images.append(image_query)
    book_query.genres.append(genre_query)
    db.session.commit()

    return jsonify(book_schema.dump(book_query)), 201


# @authenticate
def books_get_all(req) -> Response:
    query = db.session.query(Books).all()

    return jsonify(books_schema.dump(query)), 200


# @authenticate
def book_get_by_id(req, book_id) -> Response:
    query = db.session.query(Books).filter(Books.book_id == book_id).first()

    return jsonify(book_schema.dump(query)), 200


# @authenticate
def book_update_by_id(req, book_id) -> Response:
    post_data = req.form if req.form else req.json

    query = db.session.query(Books).filter(Books.book_id == book_id).first()

    if query:

        populate_object(query, post_data)

    try:

        db.session.commit()

    except:

        db.session.rollback()

        return jsonify(f"message: book with book_id {book_id} unable to update"), 400
    
    return jsonify({"message": "book updated successfully", "book": book_schema.dump(query)}), 200


# @authenticate
def book_activity(req, book_id) -> Response:
    query = db.session.query(Books).filter(Books.book_id == book_id).first()

    if query:
        query.active = not query.active

        try:

            db.session.commit()

            if query.active:

                return jsonify("record activated successfully"), 200
            
            else:

                return jsonify("record deactivated successfully"), 200
            
        except:

            db.session.rollback()

            if query.active:

                return jsonify("record activated unsuccessfully"), 400
            
            else:

                return jsonify("record deactivated unsuccessfully"), 400
            
    else:

        return jsonify(f"book with the book_id {book_id} not found"), 404
    

# @authenticate
def book_delete_by_id(req, book_id) -> Response:
    book_query = db.session.query(Books).filter(Books.book_id == book_id).first()

    try:

        db.session.delete(book_query)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: unable to delete book")
    
    return jsonify(f"book with book_id {book_id} was deleted successfully"), 200




