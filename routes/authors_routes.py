from flask import request, Response, Blueprint

from controllers import authors_controller

author = Blueprint("authors", __name__)

@author.route("/author", methods=["POST"])
def author_add() -> Response:
    return authors_controller.author_add(request)

@author.route("/authors", methods=["GET"])
def authors_get_all() -> Response:
    return authors_controller.authors_get_all(request)

@author.route("/author/<author_id>", methods=["GET"])
def author_get_by_id(author_id) -> Response:
    return authors_controller.author_get_by_id(request, author_id)

@author.route("/author/<author_id>", methods=["PUT"])
def author_update_by_id(author_id) -> Response:
    return authors_controller.author_update_by_id(request, author_id)

@author.route("/author/<author_id>", methods=["PATCH"])
def author_activity(author_id) -> Response:
    return authors_controller.author_activity(request, author_id)

@author.route("/author/<author_id>", methods=["DELETE"])
def author_delete_by_id(author_id) -> Response:
    return authors_controller.author_delete_by_id(request, author_id)