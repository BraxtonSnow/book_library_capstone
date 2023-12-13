from flask import jsonify, Response
from flask_bcrypt import generate_password_hash

from db import db 
from util.reflection import populate_object
from models.genres import Genres, genres_schema, genre_schema



def genre_add(req) -> Response:
    post_data = req.form if req.form else req.json
    genre_name = post_data.get("genre_name")

    new_record = Genres.get_new_genre()

    populate_object(new_record, post_data)


    try:

        db.session.add(new_record)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: could not add genre"), 400
    
    query = db.session.query(Genres).filter(Genres.genre_name == genre_name).first()

    return jsonify(genre_schema.dump(query)), 201


def genres_get_all(req) -> Response:
    query = db.session.query(Genres).all()

    return jsonify(genres_schema.dump(query)), 200


def genre_get_by_id(req, genre_id) -> Response:
    query = db.session.query(Genres).filter(Genres.genre_id == genre_id).first()

    return jsonify(genre_schema.dump(query)), 200


def genre_update_by_id(req, genre_id) -> Response:
    post_data = req.form if req.form else req.json

    query = db.session.query(Genres).filter(Genres.genre_id == genre_id).first()

    if query:

        populate_object(query, post_data)

    try:

        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: unable to update record"), 400
    
    return jsonify({"message": "record updated successfully", "genre": genre_schema.dump(query)}), 200


def genre_activity(req, genre_id) -> Response:
    query = db.session.query(Genres).filter(Genres.genre_id == genre_id).first()

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

        return jsonify(f"genre with the genre_id {genre_id} not found"), 404
    

def genre_delete_by_id(req, genre_id) -> Response:
    genre_query = db.session.query(Genres).filter(Genres.genre_id == genre_id).first()

    try:

        db.session.delete(genre_query)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: record could not be deleted"), 400
    
    return jsonify(f"genre with genre_id {genre_id} was deleted successfully"), 200


