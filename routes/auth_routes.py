from flask import Blueprint, Response, request

from controllers import auth_token_controller

auth = Blueprint("auth", __name__)

@auth.route("/auth/user", methods=["POST"])
def auth_token_add() -> Response:
    return auth_token_controller.auth_token_add(request)


