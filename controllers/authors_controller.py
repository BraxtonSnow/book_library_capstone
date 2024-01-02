from flask import jsonify, Response

from db import db 
from util.reflection import populate_object
from lib.authenticate import authenticate
from models.authors import Authors, authors_schema, author_schema


@authenticate
def author_add(req, auth_info) -> Response:
    post_data = req.form if req.form else req.json
    author_name = post_data.get("author_name")

    new_record = Authors.get_new_author()

    populate_object(new_record, post_data)


    try:

        db.session.add(new_record)
        db.session.commit()

    except:

       db.session.rollback()

       return jsonify("message: could not add author"), 400

    query = db.session.query(Authors).filter(Authors.author_name == author_name).first()

    return jsonify(author_schema.dump(query)), 201


@authenticate
def authors_get_all(req, auth_info) -> Response:
    query = db.session.query(Authors).all()

    return jsonify(authors_schema.dump(query)), 200


@authenticate
def author_get_by_id(req, author_id, auth_info) -> Response:
    query = db.session.query(Authors).filter(Authors.author_id == author_id).first()

    return jsonify(author_schema.dump(query)), 200


@authenticate
def author_update_by_id(req, author_id, auth_info) -> Response:
    post_data = req.form if req.form else req.json

    query = db.session.query(Authors).filter(Authors.author_id == author_id).first()

    if query:

        populate_object(query, post_data)

    try:

        db.session.commit()
    
    except:

        db.session.rollback()

        return jsonify("message: unable to update record"), 400
    
    return jsonify({"message": "record updated successfully", "author": author_schema.dump(query)}), 200


@authenticate
def author_activity(req, author_id, auth_info) -> Response:
    query = db.session.query(Authors).filter(Authors.author_id == author_id).first()

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

        return jsonify(f"author with the author_id {author_id} not found"), 404
    

@authenticate
def author_delete_by_id(req, author_id, auth_info) -> Response:
    author_query = db.session.query(Authors).filter(Authors.author_id == author_id).first()

    try:

        db.session.delete(author_query)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("message: record could not be deleted"), 400
    
    return jsonify(f"author with author_id {author_id} was deleted successfully"), 200
    