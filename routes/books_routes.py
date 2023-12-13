from flask import request, Response, Blueprint

from controllers import books_controller

book = Blueprint("books", __name__)

@book.route("/book", methods=["POST"])
def book_add() -> Response:
    return books_controller.book_add(request)

@book.route("/books", methods=["GET"])
def books_get_all() -> Response:
    return books_controller.books_get_all(request)

@book.route("/book/<book_id>", methods=["GET"])
def book_get_by_id(book_id) -> Response:
    return books_controller.book_get_by_id(request, book_id)

@book.route("/book/<book_id>", methods=["PUT"])
def book_update_by_id(book_id) -> Response:
    return books_controller.book_update_by_id(request, book_id)

@book.route("/book/<book_id>", methods=["PATCH"])
def book_activity(book_id) -> Response:
    return books_controller.book_activity(request, book_id)

@book.route("/book/<book_id>", methods=["DELETE"])
def book_delete_by_id(book_id) -> Response:
    return books_controller.book_delete_by_id(request, book_id)