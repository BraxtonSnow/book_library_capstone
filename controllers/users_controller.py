import json

from flask import jsonify, Response
from flask_bcrypt import generate_password_hash

from db import db 
from util.reflection import populate_object
from lib.authenticate import authenticate
from models.users import Users, users_schema, user_schema




def user_add(req) -> Response:
    post_data = req.form if req.form else req.json

    print('post_data: ', post_data)

    fields = ["user_name", "email", "password"]
    req_fields = ["user_name", "email", "password"]

    values = {}

    for field in fields:
        print(post_data.keys())
        field_data = post_data.get(field)
        print(field_data)
        values[field] = field_data
        if field in req_fields and not values[field]:
            return jsonify(f"{field} is required"), 400
        
    new_user = Users.get_new_user()

    populate_object(new_user, values)

    new_user.password = generate_password_hash(new_user.password).decode("utf8")

    db.session.add(new_user)
    db.session.commit()

    user_dump = user_schema.dump(new_user)
    print("user_dump: ", user_dump)

    return jsonify(user_dump), 201


# @authenticate
def users_get_all(req) -> Response:
    query = db.session.query(Users).all()

    return jsonify(users_schema.dump(query)), 200


def user_get_by_id(req, user_id) -> Response:
    query = db.session.query(Users).filter(Users.user_id == user_id).first()

    return jsonify(user_schema.dump(query)), 200


def user_update_by_id(req, user_id) -> Response:
    post_data = req.form if req.form else req.json

    query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if query:

        populate_object(query, post_data)

    try:

        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: unable to update record"), 400
    
    return jsonify({"message": "record updated successfully", "user": user_schema.dump(query)}), 200


def user_activity(req, user_id) -> Response:
    query = db.session.query(Users).filter(Users.user_id == user_id).first()

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

        return jsonify(f"user with the user_id {user_id} not found"), 404
    

def user_delete_by_id(req, user_id) -> Response:
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    try:

        db.session.delete(user_query)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: unable to delete user"), 400
    
    return jsonify(f"user with user_id {user_id} was deleted successfully"), 200
    



