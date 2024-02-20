from application.database import db
from security import datastore
from flask import jsonify, request
from flask import current_app as app
from flask_login import current_user, login_user, logout_user

from application.models.users import Users

@app.route("/api/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": {"error": "User doesn't exist!"}}), 400
    if not user.match_password(password):
        return jsonify({"message": {"error": "Wrong password"}}), 400
    if current_user.is_authenticated:
        logout_user()
    login_user(user)
    return jsonify({
        "status": "ok",
        "auth_token":user.get_auth_token(),
        "user_id": user.id,
        "username": user.name, 
        "email": user.email,
        'message': {'success':f'Welcome {user.name}!'}
    }), 200


@app.route("/api/logout", methods=["POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message':{'success':'Logout Successfull'}}), 200
    else:
        return jsonify({'message':{'error': 'Please Login first!'}}), 400
    

@app.route("/test2", methods=["GET"])
def test():
    return "Hello World!", 200