from flask import request, Response, Blueprint

from controllers import users_controller

user = Blueprint("users", __name__)



@user.route("/user", methods=["POST"])
def user_add() -> Response:
    print("hi")
    return users_controller.user_add(request)

@user.route("/users", methods=["GET"])
def users_get_all() -> Response:
    return users_controller.users_get_all(request)

@user.route("/user/<user_id>", methods=["GET"])
def user_get_by_id(user_id) -> Response:
    return users_controller.user_get_by_id(request, user_id)

@user.route("/user/<user_id>", methods=["PUT"])
def user_update_by_id(user_id) -> Response:
    return users_controller.user_update_by_id(request, user_id)

@user.route("/user/<user_id>", methods=["PATCH"])
def user_activity(user_id) -> Response:
    return users_controller.user_activity(request, user_id)

@user.route("/user/<user_id>", methods=["DELETE"])
def user_delete_by_id(user_id) -> Response:
    return users_controller.user_delete_by_id(request, user_id)


