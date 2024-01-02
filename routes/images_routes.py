from flask import request, Response, Blueprint

from controllers import images_controller

image = Blueprint("images", __name__)

@image.route("/image", methods=["POST"])
def image_add() -> Response:
    # print("request :", request)
    return images_controller.image_add(request)

@image.route("/images", methods=["GET"])
def images_get_all() -> Response:
    return images_controller.images_get_all(request)

@image.route("/image/<image_id>", methods=["GET"])
def image_get_by_id(image_id) -> Response:
    return images_controller.image_get_by_id(request, image_id)

@image.route("/image/<image_id>", methods=["PUT"])
def image_update_by_id(image_id) -> Response:
    return images_controller.image_update_by_id(request, image_id)

@image.route("/image/<image_id>", methods=["PATCH"])
def image_activity(image_id) -> Response:
    return images_controller.image_activity(request, image_id)

@image.route("/image/<image_id>", methods=["DELETE"])
def image_delete_by_id(image_id) -> Response:
    return images_controller.image_delete_by_id(request, image_id)