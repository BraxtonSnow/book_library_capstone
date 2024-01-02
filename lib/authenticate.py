from functools import wraps
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from flask import Response, jsonify, request

from db import db 
from models.auth_tokens import AuthTokens


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)
        
        return True
    
    except:

        return False
    

def validate_token(args):
    print(args.headers)
    auth_token = args.headers["Auth-Token"]

    if not auth_token or not validate_uuid4(auth_token):

        return False
    
    existing_token = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).first()

    if existing_token:
        if existing_token.expiration > datetime.now():
            return existing_token
    else:
        return False
    

def fail_response():
    return Response("authentication required", 401)


# def authenticate(func):
#     @wraps(func)
#     def wrapper_auth_return(*args, **kwargs):
#         auth_info = request.headers.get("Auth-Token")

#         auth_token = db.session.query()

#         if not auth_info:
#             return func(*args, **kwargs)
#         else:
#             return fail_response()
#     return wrapper_auth_return


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_token = request.headers.get("Auth-Token")
        if not auth_token:
            return jsonify({"error": "auth_token missing"}), 401
        
        auth_record = AuthTokens.query.filter_by(auth_token=auth_token).first()
        
        if not auth_record:
            return jsonify({"error": "Invalid auth_token"}), 401
        
        current_time = datetime.utcnow()
        if auth_record.expiration and auth_record.expiration < current_time:
            return jsonify({"error": "Expired auth_token"}), 401
        
        return func(auth_info=auth_record, *args, **kwargs)
    
    return wrapper