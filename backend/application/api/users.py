from flask_restful import Resource, fields, marshal, reqparse
from application.database import db
from security import datastore
from flask import request, jsonify
# from flask_login import login_user, logout_user, current_user
from flask_security import auth_token_required, roles_required

from application.models.users import Users
from utils.credentials import *

class UserRegister(Resource):    
    ## Register new User
    def post(self): 
        formData = request.form.to_dict()
        ## Check if email is NOT in Users database
        if not Users.query.filter_by(email=formData['email']).first():
            ## If NOT valid email (utils)
            if not validate_email(formData['email']):
                return {'message': {'error': 'Invalid Email'}}, 400
            ## If NOT valid password (utils)
            elif not validate_password(formData['password']):
                return {'message': {'error': 'Password must have atleast one Upper Case Letter,\
                                     Lower Case Letter, Special Character and a number.\
                                    Password must have 8 or more characters.'}}, 400
            else:
                user = datastore.create_user(email=formData['email'], name=formData['name'],
                                           password=hash_password(formData['password']))
                datastore.add_role_to_user(user, 'user')
                db.session.add(user)
                db.session.commit()
                return {'message': {'success': 'Registration Successfull, Login Now!'}}, 200
        # Email present in Users database
        return {'message': {'error': 'Email already exists.'}}, 400
