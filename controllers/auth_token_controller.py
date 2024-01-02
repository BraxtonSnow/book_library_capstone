from flask import jsonify, request
from flask_bcrypt import check_password_hash

from datetime import datetime, timedelta

from models.users import Users
from models.auth_tokens import AuthTokens, auth_token_schema
from db import db 

def auth_token_add(req):
    if req.content_type == "application/json":
        # print("function", "I ran function")
        post_data = req.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
 
        user_data = db.session.query(Users).filter(Users.email == email).first()

        if user_data and check_password_hash(user_data.password, password):
            expiration = datetime.utcnow() + timedelta(minutes=5)
            new_auth_token = AuthTokens(user_id=user_data.user_id, expiration=expiration)

            db.session.add(new_auth_token)
            db.session.commit()

            return jsonify({"message": "auth-token added", "auth": auth_token_schema.dump(new_auth_token)}), 201
        else:
            return jsonify({"error": "Invalid email/password"}), 401
        

def auth_token_remove(req):
    post_data = req.get_json()
    print("post_data", post_data)
    auth_token = None
    if post_data:
        auth_token = post_data.get("auth_token")
    
    auth_record = AuthTokens.query.filter_by(auth_token=auth_token).first()
    
    if auth_record:
        db.session.delete(auth_record)
        db.session.commit()
        return jsonify({"message": "Authentication token removed"}), 200
    else:
        return jsonify({"error": "Authentication token not found"}), 404

def auth_token_remove_expired(req: request):
    expired_auth_tokens = AuthTokens.query.filter(AuthTokens.expiration < datetime.utcnow()).all()
    
    for auth_token in expired_auth_tokens:
        db.session.delete(auth_token)
    
    db.session.commit()
    
    return jsonify({"message": f"Removed {len(expired_auth_tokens)} expired authentication tokens"}), 200







        # if not values["email"] or not values["password"] or not user_data:
        #     return jsonify({"message: invalid login"}), 401

        # if user_data:
        #     is_password_valid = check_password_hash(user_data.password, password)
        #     if is_password_valid == False:
        #         return jsonify({"message", "Invalid email/password"}), 401
            

        
        # valid_password = check_password_hash(user_data.password, values["password"])

        # if not valid_password:
        #     return jsonify({"message": "invalid login"}), 401
        
        # existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_data.user_id).all()

        # expiry = datetime.now() + timedelta(hours=12)

        # if existing_tokens:
        #     for token in existing_tokens:
        #         if token.expiration < datetime.now():
        #             db.session.delete(token)

        # new_token = AuthTokens(user_data.user_id, expiry)
        # db.session.add(new_token)
        # db.session.commit()

        # return jsonify({"message": {"auth_token": auth_token_schema.dump(new_token)}})