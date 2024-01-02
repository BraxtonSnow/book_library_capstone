from flask import request, Response, Blueprint

from controllers import genres_controller

genre = Blueprint("genres", __name__)

@genre.route("/genre", methods=["POST"])
def genre_add() -> Response:
    print("genre: ", request)
    return genres_controller.genre_add(request)

@genre.route("/genres", methods=["GET"])
def genres_get_all() -> Response:
    return genres_controller.genres_get_all()

@genre.route("/genre/<genre_id>", methods=["GET"])
def genre_get_by_id(genre_id) -> Response:
    return genres_controller.genre_get_by_id(request, genre_id)

@genre.route("/genre/<genre_id>", methods=["PUT"])
def genre_update_by_id(genre_id) -> Response:
    return genres_controller.genre_update_by_id(request, genre_id)

@genre.route("/genre/<genre_id>", methods=["PATCH"])
def genre_activity(genre_id) -> Response:
    print("i have made it i think")
    return genres_controller.genre_activity(genre_id)

@genre.route("/genre/<genre_id>", methods=["DELETE"])
def genre_delete_by_id(genre_id) -> Response:
    print("i have made it i think")
    return genres_controller.genre_delete_by_id(genre_id)