from flask import jsonify, Response

from db import db 
from util.reflection import populate_object
from models.images import Images, images_schema, image_schema



def image_add(req) -> Response:
    post_data = req.form if req.form else req.json
    image_name = post_data.get("image_name")

    new_record = Images.get_new_image()

    populate_object(new_record, post_data)


    try:

        db.session.add(new_record)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: could not add image")

    query = db.session.query(Images).filter(Images.image_name == image_name).first()

    return jsonify(image_schema.dump(query)), 201


def images_get_all(req) -> Response:
    query = db.session.query(Images).all()

    return jsonify(images_schema.dump(query)), 200


def image_get_by_id(req, image_id) -> Response:
    query = db.session.query(Images).filter(Images.image_id == image_id).first()

    return jsonify(image_schema.dump(query)), 200


def image_update_by_id(req, image_id) -> Response:
    post_data = req.form if req.form else req.json

    query = db.session.query(Images).filter(Images.image_id == image_id).first()

    if query:

        populate_object(query, post_data)

    try:

        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: unable to update record"), 400
    
    return jsonify({"message": "record updated successfully", "image": image_schema.dump(query)}), 200


def image_activity(req, image_id) -> Response:
    query = db.session.query(Images).filter(Images.image_id == image_id).first()

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

        return jsonify(f"image with image_id {image_id} not found"), 404
    

def image_delete_by_id(req, image_id) -> Response:
    image_query = db.session.query(Images).filter(Images.image_id == image_id).first()

    try:

        db.session.delete(image_query)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: record could not be deleted"), 400
    
    return jsonify(f"image with image_id {image_id} was deleted successfully"), 200


        
   

    
